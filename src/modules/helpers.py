import pandas as pd
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
