import pandas as pd


def reduce_col(df, on, column, function):
    '''Reduces a dataframe to have unique values in the 'on' column,
    as in SQL GROUP BY, and aggregated values in 'column' based on a
    function.

    Params
    ------
    df: dataframe
        Contains the unaggregated data
    on: string, int
        Column key, specifies the column to group values by
    column: string, int
        Column key, specifies the column of which to aggregate values
    function: function
        How to aggregate the values

    Returns
    -------
    A series with unique values in column `on` as the index',
    and aggregated values in columns `column` based on `function`.
    '''

    cols = [on, column]
    try:
        assert False not in [col in df.columns for col in cols], \
            'Columns provided are not in the dataframe provided.'
    except AssertionError:
        print('Cannot create new dataframe')
        raise

    return function(df.groupby(on)[column])


def reduce_cols(df, index, columns, function):
    '''Applies aggregation to multiple columns.

    Params
    ------
    df: dataframe
        Contains the unaggregated data
    index: string, int
        Column key, specifies the column to group values by
    columns: list
        Column keys, specifies the column of which to aggregate values
    function: function
        How to aggregate the values

    Returns
    -------
    A dataframe with `index` as the index',
    and aggregated values in `columns` based on `function`.
    '''

    data = {}

    for col in columns:
        s = reduce_col(df, index, col, lambda x: x.apply(function))
        data['total_' + s.name] = s

    return pd.DataFrame(data).reset_index()
