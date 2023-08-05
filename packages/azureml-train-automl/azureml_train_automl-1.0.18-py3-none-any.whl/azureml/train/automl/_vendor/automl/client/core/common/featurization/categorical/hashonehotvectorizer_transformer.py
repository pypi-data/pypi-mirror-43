# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
"""Convert input to hash and encode to one hot encoded vector."""
from typing import Optional, Union
from logging import Logger
import numpy as np
from scipy import sparse
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.utils import murmurhash3_32

from automl.client.core.common.logging_utilities import function_debug_log_wrapped
from automl.client.core.common.featurization.logger import TransformerLogger


class HashOneHotVectorizerTransformer(BaseEstimator, TransformerMixin, TransformerLogger):
    """Convert input to hash and encode to one hot encoded vector."""

    def __init__(self,
                 hashing_seed_val: int,
                 num_cols: int = 8096,
                 logger: Optional[Union[Logger, TransformerLogger]] = None):
        """
        Initialize for hashing one hot encoder transform with a seed value and maximum number of expanded columns.

        :param hashing_seed_val: Seed value for hashing transform.
        :param num_cols: Number of columns to be generated.
        :param logger: Logger to be injected to usage in this class.
        :return:
        """
        self._num_cols = num_cols
        self._seed = hashing_seed_val
        self._init_logger(logger)

    def fit(self, x, y=None):
        """
        Fit function for hashing one hot encoder transform.

        :param x: Input array.
        :type x: numpy.ndarray or pandas.series
        :param y: Target values.
        :type y: numpy.ndarray
        :return: The instance object: self.
        """
        return self

    def _hash_cat_feats(self, x):
        """
        Hash transform and one-hot encode the input series or dataframe.

        :param x: Series that represents column.
        :type x: numpy.ndarray or pandas.series
        :return: Hash vector features for column.
        """
        row = []
        col = []
        data = []
        row_no = 0
        for val in x:
            hash_val = murmurhash3_32(val, self._seed) % self._num_cols
            row.append(row_no)
            row_no = row_no + 1
            col.append(hash_val)
            data.append(True)

        X = sparse.csr_matrix((data, (row, col)),
                              shape=(x.shape[0], self._num_cols),
                              dtype=np.bool_)
        X.sort_indices()
        return X

    @function_debug_log_wrapped
    def transform(self, x):
        """
        Transform function for hashing one hot encoder transform.

        :param x: Input array.
        :type x: numpy.ndarray or pandas.series
        :return: Result of hashing one hot encoder transform.
        """
        return self._hash_cat_feats(x)
