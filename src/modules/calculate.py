def estimate_floor_area(data, column_map, ref_vals):
    '''Estimates the floor area of countries.

    Params
    ------
    data: pandas dataframe
        The dataset used for the calculation
    column_map: dictionary
        A column mapping in the form
        {
            'pd_i': <original column name for population density from country i>,
            'ca_i: <original column name for country area from country i>
        }
    ref_vals: dictionary
        reference values in the form
        {
            'fa_r': <floor area from the reference country value>,
            'ca_r':  <country area from the reference country value>,
            'pd_r': <population density from the reference country value>,
        }

    Returns
    -------
    pandas datframe
        a copy of the original data with a new column containing the estimates

    Notes:
    ------
    Estimates is based on the predictors:

    .. math::
        area_ratio = \frac{fa_r}{ca_r}
        population_ratio = \frac{pd_i}{pd_r}

    where
    :math: `fa_r` is the floor area from the reference country
    :math: `ca_r` is the country area from the reference country
    :math: `pd_r` is the population density from the reference country
    :math: `pd_i` is the population density from country :math: `i`


    The estimated floor area is then:

    .. math::
        estimated_floor_area = area_ratio * population_ratio * ca_i

    where
    :math: `ca_i` is the country area from the country :math: `i`

    This formula can also be thought of in terms of a 'baseline ratio':

    .. math::
        baseline_ratio = area_ratio * \frac{population_ratio}{pd_i}
        estimated_floor_area = baseline_ratio * pd_i * ca_i

    This is designed with a single reference country in mind.
    Attention! Make sure the inputs to the ratios all have the same units!
    '''

    _d = data.copy()
    cm = {}

    try:
        for key in column_map:
            cm[column_map[key]] = key
        _d = _d.rename(columns=cm)
        area_ratio = ref_vals['fa_r'] / ref_vals['ca_r']
        pd_r = ref_vals['pd_r']
    except Exception as e:
        print('Check input values!', e)

    _d['population_ratio'] = _d['pd_i'] / pd_r
    _d['estimated_floor_area'] = area_ratio * _d['population_ratio'] * _d['ca_i']

    _data = data.copy()
    _data['estimated_floor_area'] = _d['estimated_floor_area']

    return _data


def calculate_emissions(data, column_map):
    '''Estimates the emissions of countries.

    Params
    ------
    data: pandas dataframe
        The dataset used for the calculation
    column_map: dictionary
        A column mapping in the form
        {
            'area': <original column name for estimated floor area of area i>,
            'heating_demand': <original column name for heating demand factor for country i>,
            'ohfa': <original column name for on-site heated floor area factor of country i>,
            'emission: <original column name for emission factor for country i>
        }

    Returns
    -------
    pandas datframe
        a copy of the original data with a new column containing the estimates

    Notes:
    ------
    Emissions are estimated based on the following formula:

    .. math::
        estimated_emissions = area * ohfa * heating_demand * emission

    where
    :math: `area` is the estimated floor area of area :math: `i`
    :math: `ohfa` is the on-site heated floor area factor of country :math: `i`
    :math: `heating_demand` is the heating demand factor in GWh per meters squared for country :math: `i`
    :math: `emission` is the emission factor in tonnes CO2 per GWh for country :math: `i`
    '''

    _d = data.copy()
    cm = {}

    try:
        for key in column_map:
            cm[column_map[key]] = key
        _d = _d.rename(columns=cm)
    except Exception as e:
        print('Check input values!', e)

    _d['estimated_emissions'] = _d['area'] * _d['ohfa'] * _d['heating_demand'] * _d['emission']

    _data = data.copy()
    _data['estimated_emissions'] = _d['estimated_emissions']

    return _data
