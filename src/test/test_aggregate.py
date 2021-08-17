import pandas as pd
import numpy as np
import numpy.random as npr
import pytest
import sys
import os

sys.path.append(os.path.abspath(os.path.join('..', '..', 'src')))
from modules.aggregate import Aggregate

class TestAggregate:

    @pytest.fixture
    def df1(self):
        rows, col_names = 1000, ['0', '1']
        cols = npr.rand(rows, len(col_names))
        return pd.DataFrame(cols, columns=col_names)

    @pytest.fixture
    def df2(self):
        rows, col_names = 1000, ['0', '1', '2']
        cols = npr.rand(rows, len(col_names))
        return pd.DataFrame(cols, columns=col_names)

    def test_combine_continents(self, df1, df2):
        '''Check new dataset is correct length.'''
        combined = Aggregate.combine_continents(df1, df2, columns=['0'])
        assert len(combined) == len(set(df1['0']).union(df2['0']))

    def test_add_cols(self, df1, df2):
        '''Tests that added column has no na values'''
        index = df1.index
        df1['index'] = index
        df2['index'] = index
        combined = Aggregate.add_cols(df1, df2, on='index', cols='2')
        assert np.any(combined['2'].isna()) == False
