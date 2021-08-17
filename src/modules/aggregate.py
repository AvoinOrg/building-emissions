class Aggregate:
    '''Joins datasets to create one master data table.
    Note: the master country list is 'climatetrace_countries'.
    '''

    def combine_continents(ne_countries_continents, manual_continents_data, columns, X='last'):
        ''' Adds countries and continent information from `manual_continents_data`
        to `ne_countries_continents` and overwritres any overlapping countries.

        Params
        ------
        ne_countries_continents: dataframe with countries and continents to add to
        manual_continents_data: dataframe with countries and continents to update from
        columns: list of columns to drop duplicates from
        X: strategy for dropping duplicates {'first', 'last', None} -- see pandas docs

        Returns
        -------
        datframe with updated continent information for countries
        from union(ne_countries_continents.iso3_code, manual_continents_data.iso3_code)
        '''

        all_continents = ne_countries_continents.append(manual_continents_data, ignore_index=True)

        return all_continents.drop_duplicates(subset=columns, keep=X).reset_index(drop=True)

    def add_cols(df, other, on, cols=None, drop=False):
        ''' Adds On-site heated floor area factors to countries based on continent information.
        Like an SQL left join.

        Params
        ------
        df: dataframe to add onto
        on: column from df and other to use as add key
        other: dataframe to add columns from
        cols: list of columns to add, if None adds all
        drop: False, if True drops the intermediate columns (the column added 'on')

        Returns
        -------
        copy of df datframe with new columns added
        '''

        if cols is not None:
            other = other.set_index(on)[cols]
        else:
            other = other.set_index(on)

        try:
            _df = df.join(other, on=on)
        except Exception as e:
            print(e)

        if drop:
            return _df.drop(on, axis=1)
        return _df
