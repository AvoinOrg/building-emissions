import pandas as pd
import numpy as np
from IPython.display import display


def show_all(df, rows=True, cols=True):
    '''Updates the pandas display options with a context manage to show
    all rows/columns of a dataframe.

    Params
    ------
    df: dataframe to show
    rows: boolean, if True shows all rows
    columns: boolean, if True shows all columns
    '''

    if rows and cols:
        with pd.option_context('display.max_rows', None, 'display.max_columns', None):
            display(df)
    elif rows:
        with pd.option_context('display.max_rows', None):
            display(df)
    elif cols:
        with pd.option_context('display.max_columns', None):
            display(df)


def print_na(df, cols, v=False):
    '''Check that all countries have data in new columns.

    Params
    ------
    df: aggregated dataframe
    col: list of newly added column names
    v: boolean, toggel verbosity
    '''

    for col in cols:
        nas = df[col].isna()
        print('\nNumber of NA values in column {}:\n {}\n***'.format(col, np.sum(nas)))
        v and show_all(df[nas].reindex())
