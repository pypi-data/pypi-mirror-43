# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
"""Class for timeseries preprocessing."""
from collections import defaultdict
import copy
import inspect
import json
import warnings
import numpy as np
import pandas as pd

from sklearn.base import BaseEstimator, TransformerMixin

from automl.client.core.common.constants import TimeSeries, TimeSeriesInternal
from automl.client.core.common.featurization.logger import TransformerLogger
from automl.client.core.common.featurization.timeseries.rolling_window import RollingWindow
from automl.client.core.common.featurization.timeseries.lag_lead_operator import LagLeadOperator
from automl.client.core.common.featurization.timeseries.missingdummies_transformer import MissingDummiesTransformer
from automl.client.core.common.featurization.timeseries.numericalize_transformer import NumericalizeTransformer
from automl.client.core.common.featurization.timeseries.abstract_timeseries_transformer \
    import AbstractTimeSeriesTransformer
from automl.client.core.common._engineered_feature_names import \
    _GenerateEngineeredFeatureNames, \
    _TransformationFunctionNames, _OperatorNames, \
    FeatureTypeRecognizer, _Transformer, \
    _FeatureTransformers, _FeatureNameJSONTag


# Prevent warnings when using Jupyter
warnings.simplefilter("ignore")
pd.options.mode.chained_assignment = None


class TimeSeriesTransformer(AbstractTimeSeriesTransformer):
    """Class for timeseries preprocess."""

    def __init__(self, logger=None, **kwargs):
        """
        Construct for the class.

        :param logger: The logger to be used in the pipeline.
        :type logger: logging.Logger
        :param kwargs: dictionary contains metadata for TimeSeries.
                       time_column_name: The column containing dates.
                       grain_column_names: The set of columns defining the
                       multiple time series.
                       origin_column_name: latest date from which actual values
                       of all features are assumed to be known with certainty.
                       drop_column_names: The columns which will needs
                       to be removed from the data set.
                       group: the group column name.
        :type kwargs: dict

        """
        self._transforms = {}
        if TimeSeriesInternal.LAGS_TO_CONSTRUCT in kwargs.keys():
            self._get_transformer_params(LagLeadOperator,
                                         TimeSeriesInternal.LAG_LEAD_OPERATOR,
                                         **kwargs)
        if TimeSeriesInternal.WINDOW_SIZE in kwargs.keys() and TimeSeriesInternal.TRANSFORM_DICT in kwargs.keys():
            self._get_transformer_params(RollingWindow,
                                         TimeSeriesInternal.ROLLING_WINDOW_OPERATOR,
                                         **kwargs)
        super(TimeSeriesTransformer, self).__init__(logger, **kwargs)

    def _get_transformer_params(self, cls, name, **kwargs):
        """
        Create the transformer if type cls and put it to the self._transforms with label name.

        :param cls: the class of transformer to be constructed.
        :type cls: type
        :param name: Transformer label.
        :type name: str
        :param kwargs: the dictionary of parameters to be parsed.
        :type kwargs: dict

        """
        rw = {}
        valid_args = inspect.getargspec(cls.__init__)[0]
        for k, v in kwargs.items():
            if k in valid_args:
                rw[k] = v

        self._transforms[name] = cls(**rw)

    def _construct_pre_processing_pipeline(self, tsdf, drop_column_names):
        """Return the featurization pipeline."""
        from .forecasting_pipeline import AzureMLForecastPipeline
        from .grain_index_featurizer import GrainIndexFeaturizer
        from .time_series_imputer import TimeSeriesImputer
        from .time_index_featurizer import TimeIndexFeaturizer

        numerical_columns = [x for x in tsdf.select_dtypes(include=[np.number]).columns
                             if x not in drop_column_names]
        if self.target_column_name in numerical_columns:
            numerical_columns.remove(self.target_column_name)
        if self.original_order_column in numerical_columns:
            numerical_columns.remove(self.original_order_column)

        imputation_dict = {col: tsdf[col].median() for col in numerical_columns}
        impute_missing_numerical_values = TimeSeriesImputer(
            input_column=numerical_columns, value=imputation_dict, freq=self.freq)

        time_index_featurizer = TimeIndexFeaturizer(overwrite_columns=True)

        categorical_columns = [x for x in tsdf.select_dtypes(['object', 'category', 'bool']).columns
                               if x not in drop_column_names]
        if self.group_column in categorical_columns:
            categorical_columns.remove(self.group_column)

        # pipeline:
        default_pipeline = AzureMLForecastPipeline([
            ('make_numeric_na_dummies', MissingDummiesTransformer(numerical_columns)),
            ('impute_na_numeric_columns', impute_missing_numerical_values),
            ('make_time_index_featuers', time_index_featurizer)
        ])

        # To get the determined behavior sort the self._transforms.
        transforms_ordered = sorted(self._transforms.keys())
        for transform in transforms_ordered:
            # Add the transformer to the default pipeline
            default_pipeline.add_pipeline_step(transform, self._transforms[transform])

        # Don't apply grain featurizer when there is single timeseries
        if self.dummy_grain_column not in self.grain_column_names:
            grain_index_featurizer = GrainIndexFeaturizer(overwrite_columns=True)
            default_pipeline.add_pipeline_step('make_grain_features', grain_index_featurizer)

        default_pipeline.add_pipeline_step('make_categoricals_numeric', NumericalizeTransformer())
        return default_pipeline

    def _create_feature_transformer_graph(self, graph, feature_from, feature_to, transformer):
        """
        Add the each feature's transform procedure into the graph.

        :param graph: a dictionary contains feature's transformer path
        :type graph: dict
        :param feature_from: feature name before transform
        :type feature_from: str
        :param feature_to: feature name after transform
        :type feature_to: str
        :param transformer: the name of transformer processed the feature
        :type transformer: str
        """
        if feature_to in graph:
            graph[feature_to].append([feature_from, transformer])
        else:
            if feature_from in graph:
                # Deep copy the feature's pre transformers
                graph[feature_to] = copy.deepcopy(graph[feature_from])
                graph[feature_to].append([feature_from, transformer])
            else:
                graph[feature_to] = [[feature_from, transformer]]

    def _generate_json_for_engineered_features(self, tsdf):
        """
        Create the transformer json format for each engineered feature.

        :param graph: a dictionary contains feature's transformer path
        :type graph: dict
        """
        # Create the feature transformer graph from pipeline's steps
        # The dict contains key-> list, list includes a series of transformers
        graph = defaultdict(list)
        for name, transformer in self.pipeline._steps:
            if name == TimeSeriesInternal.MAKE_NUMERIC_NA_DUMMIES:
                for col in transformer.numerical_columns:
                    self._create_feature_transformer_graph(graph, col, col + '_WASNULL', name)
            elif name == TimeSeriesInternal.IMPUTE_NA_NUMERIC_COLUMNS:
                for col in transformer.input_column:
                    self._create_feature_transformer_graph(graph, col, col, name)
            elif name == TimeSeriesInternal.MAKE_TIME_INDEX_FEATURES:
                for col in transformer.preview_time_feature_names(tsdf):
                    self._create_feature_transformer_graph(graph, tsdf.time_colname, col, name)
            elif name == TimeSeriesInternal.MAKE_GRAIN_FEATURES:
                for col in tsdf.grain_colnames:
                    self._create_feature_transformer_graph(graph, col, 'grain_' + col, name)
            elif name == TimeSeriesInternal.MAKE_CATEGORICALS_NUMERIC:
                for col in transformer._categories_by_col.keys():
                    self._create_feature_transformer_graph(graph, col, col, name)
            elif name in [TimeSeriesInternal.LAG_LEAD_OPERATOR, TimeSeriesInternal.ROLLING_WINDOW_OPERATOR]:
                for col in transformer.preview_column_names(tsdf):
                    features = None
                    if name == TimeSeriesInternal.LAG_LEAD_OPERATOR:
                        features = transformer.lags_to_construct.keys()
                    else:
                        features = transformer.transform_dict.values()
                    raw_feature = tsdf.ts_value_colname
                    for feature in features:
                        if col.startswith(feature):
                            raw_feature = feature
                    self._create_feature_transformer_graph(graph, raw_feature, col, name)

        for engineered_feature_name in self.engineered_feature_names:
            col_transformers = graph.get(engineered_feature_name, [])
            transformers = []
            val = ''
            for col, transformer in col_transformers:
                input_feature = col
                # for each engineered feature's transform path, only store the first transformer's
                # input which is raw feature name, other transformers' input are previous transformer
                if len(transformers) > 0:
                    input_feature = len(transformers)
                if transformer == TimeSeriesInternal.MAKE_NUMERIC_NA_DUMMIES:
                    transformers.append(
                        _Transformer(
                            parent_feature_list=[input_feature],
                            transformation_fnc=_TransformationFunctionNames.ImputationMarker,
                            operator=None,
                            feature_type=FeatureTypeRecognizer.Numeric,
                            should_output=True)
                    )
                elif transformer == TimeSeriesInternal.IMPUTE_NA_NUMERIC_COLUMNS:
                    transformers.append(
                        _Transformer(
                            parent_feature_list=[input_feature],
                            transformation_fnc=_TransformationFunctionNames.Imputer,
                            operator=_OperatorNames.Mean,
                            feature_type=FeatureTypeRecognizer.Numeric,
                            should_output=True)
                    )
                elif transformer == TimeSeriesInternal.MAKE_TIME_INDEX_FEATURES:
                    transformers.append(
                        _Transformer(
                            parent_feature_list=[input_feature],
                            transformation_fnc=_TransformationFunctionNames.DateTime,
                            operator=None,
                            feature_type=FeatureTypeRecognizer.DateTime,
                            should_output=True)
                    )
                    val = engineered_feature_name
                elif transformer == TimeSeriesInternal.MAKE_GRAIN_FEATURES:
                    transformers.append(
                        _Transformer(
                            parent_feature_list=[input_feature],
                            transformation_fnc=_TransformationFunctionNames.GrainMarker,
                            operator=None,
                            feature_type=FeatureTypeRecognizer.Ignore,
                            should_output=True)
                    )
                elif transformer == TimeSeriesInternal.MAKE_CATEGORICALS_NUMERIC:
                    transformers.append(
                        _Transformer(
                            parent_feature_list=[input_feature],
                            transformation_fnc=_TransformationFunctionNames.LabelEncoder,
                            operator=None,
                            feature_type=FeatureTypeRecognizer.Categorical,
                            should_output=True)
                    )
                elif transformer == TimeSeriesInternal.LAG_LEAD_OPERATOR:
                    # engineered_feature_name of lag operation is %target_col_name%_lags%size%%period"
                    # put the %size%%period% to val
                    val = engineered_feature_name[(len(col) + 4):]
                    transformers.append(
                        _Transformer(
                            parent_feature_list=[input_feature],
                            transformation_fnc=_TransformationFunctionNames.Lag,
                            operator=None,
                            feature_type=FeatureTypeRecognizer.Numeric,
                            should_output=True)
                    )
                elif transformer == TimeSeriesInternal.ROLLING_WINDOW_OPERATOR:
                    # engineered_feature_name of rollingwindow operation is %target_col_name%_func%size%%period"
                    # put the %size%%period% to val
                    func_value = engineered_feature_name[len(col) + 1:].split("_", 2)
                    func = func_value[0]
                    val = func_value[1]
                    transformers.append(
                        _Transformer(
                            parent_feature_list=[input_feature],
                            transformation_fnc=_TransformationFunctionNames.RollingWindow,
                            operator=func,
                            feature_type=FeatureTypeRecognizer.Numeric,
                            should_output=True)
                    )

            feature_transformers = _FeatureTransformers(transformers)
            # Create the JSON object
            transformation_json = feature_transformers.encode_transformations_from_list()
            transformation_json_data = transformation_json._entire_transformation_json_data
            transformation_json_data[_FeatureNameJSONTag.Value] = val
            self._engineered_feature_name_json_objects[engineered_feature_name] = \
                transformation_json_data

    def _get_json_str_for_engineered_feature_name(self,
                                                  engineered_feature_name):
        """
        Return JSON string for engineered feature name.

        :param engineered_feature_name: Engineered feature name for
            whom JSON string is required
        :return: JSON string for engineered feature name
        """
        # If the JSON object is not valid, then return None
        if engineered_feature_name not in self._engineered_feature_name_json_objects:
            engineered_feature_name_json_obj = []
        else:
            engineered_feature_name_json_obj = \
                self._engineered_feature_name_json_objects[engineered_feature_name]

        # Convert JSON into string and return
        return json.dumps(engineered_feature_name_json_obj)

    def get_json_strs_for_engineered_feature_names(self,
                                                   engi_feature_name_list):
        """
        Return JSON string list for engineered feature names.

        :param engi_feature_name_list: Engineered feature names for
            whom JSON strings are required
        :return: JSON string list for engineered feature names
        """
        engineered_feature_names_json_str_list = []

        # Walk engineering feature name list and get the corresponding
        # JSON string
        for engineered_feature_name in engi_feature_name_list:

            json_str = \
                self._get_json_str_for_engineered_feature_name(
                    engineered_feature_name)

            engineered_feature_names_json_str_list.append(json_str)

        # Return the list of JSON strings for engineered feature names
        return engineered_feature_names_json_str_list
