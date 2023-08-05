# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
"""Class for top level text transformation logic."""
from typing import Optional, Union, Dict, Tuple, List
import logging
import numpy as np
import pandas as pd
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer

from automl.client.core.common import constants
from automl.client.core.common.featurization.logger import TransformerLogger
from automl.client.core.common.featurization.categorical.cat_imputer import CatImputer
from .utilities import max_ngram_len
from automl.client.core.common._engineered_feature_names import _Transformer, _TransformationFunctionNames, \
    FeatureTypeRecognizer, _OperatorNames, _FeatureTransformers, _GenerateEngineeredFeatureNames
from .stringcast_transformer import StringCastTransformer
from .naive_bayes import NaiveBayes


class TextTransformer(BaseEstimator, TransformerMixin, TransformerLogger):
    """Class for top level text transformation logic."""

    def __init__(self,
                 task_type: Optional[str] = constants.Tasks.CLASSIFICATION,
                 logger: Optional[Union[logging.Logger, TransformerLogger]] = None):
        """
        Preprocessing class for Text.

        :param task_type: 'classification' or 'regression' depending on what kind of ML problem to solve.
        :param logger: The logger to use.
        """
        self._task_type = task_type
        self.logger = logger

    def get_transforms(self,
                       column: pd.DataFrame,
                       column_name: str,
                       ngram_len: int,
                       engineered_feature_names: _GenerateEngineeredFeatureNames) -> \
            List[Tuple[pd.DataFrame, List[TransformerMixin], Dict[str, str]]]:
        """
        Create a list of transforms for text data.

        :param column: Column name in the data frame.
        :param column_name: Name of the column for engineered feature names
        :param ngram_len: Continous length of characters or number of words.
        :param engineered_feature_names: Existing engineered feature names
        :return: Text transformations to use in a list.
        """
        ngram_len = min(max_ngram_len, ngram_len)

        # Add the transformations to be done and get the alias name
        # for the trichar transform.
        text_trichar_string_cast_transformer = _Transformer(
            parent_feature_list=[str(column_name)],
            transformation_fnc=_TransformationFunctionNames.StringCast,
            operator=None, feature_type=FeatureTypeRecognizer.Text,
            should_output=False)
        # This transformation depends on the previous transformation
        text_trichar_tfidf_transformer = _Transformer(
            parent_feature_list=[1],
            transformation_fnc=_TransformationFunctionNames.Tf,
            operator=_OperatorNames.CharGram, feature_type=None,
            should_output=True)
        # Create an object to convert transformations into JSON object
        feature_transformers = _FeatureTransformers([
            text_trichar_string_cast_transformer,
            text_trichar_tfidf_transformer])
        # Create the JSON object
        json_obj = feature_transformers.encode_transformations_from_list()
        # Persist the JSON object for later use and obtain an alias name
        tfidf_trichar_column_name = engineered_feature_names.get_raw_feature_alias_name(json_obj)

        # Add the transformations to be done and get the alias name
        # for the bigram word transform.
        text_biword_string_cast_transformer = _Transformer(
            parent_feature_list=[str(column_name)],
            transformation_fnc=_TransformationFunctionNames.StringCast,
            operator=None, feature_type=FeatureTypeRecognizer.Text,
            should_output=False)
        # This transformation depends on the previous transformation
        text_biword_tfidf_transformer = _Transformer(
            parent_feature_list=[1],
            transformation_fnc=_TransformationFunctionNames.Tf,
            operator=_OperatorNames.WordGram, feature_type=None,
            should_output=True)
        # Create an object to convert transformations into JSON object
        feature_transformers = _FeatureTransformers([
            text_biword_string_cast_transformer,
            text_biword_tfidf_transformer])
        # Create the JSON object
        json_obj = feature_transformers.encode_transformations_from_list()
        # Persist the JSON object for later use and obtain an alias name
        tfidf_biword_column_name = engineered_feature_names.get_raw_feature_alias_name(json_obj)

        tr = [(column,
               [
                   StringCastTransformer(logger=self.logger),
                   TfidfVectorizer(use_idf=False, norm='l2', max_df=0.95, analyzer='char', ngram_range=(1, ngram_len))
               ],
               {
                   'alias': str(tfidf_trichar_column_name)
               }
               ),
              (column,
               [
                   StringCastTransformer(logger=self.logger),
                   TfidfVectorizer(use_idf=False, norm='l2', analyzer='word', ngram_range=(1, 2))
               ],
               {
                   'alias': str(tfidf_biword_column_name)
               }
               )]

        return tr
