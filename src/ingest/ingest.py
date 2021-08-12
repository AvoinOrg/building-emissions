import sys, os
sys.path.append(os.path.abspath(os.path.join('..', 'modules')))

import read as r

class Ingest:
    '''Ingests all input data needed for the project.
    '''

    # missing areas and building statisticts
    schema = {
        'climatetrace_countries': {
            'extension': '.csv',
            'original_cols': ["name", "alpha3"],
            'renamed_cols': ["country_name", "iso3_code"],
            'col_dtypes': ["string", "string"]
        },

        'countries_data': {
            'extension': '.csv',
            'original_cols': ["Alpha-3 code", "pop_density_1overm2", "Emission factor tCO2/GWh"],
            'renamed_cols': ["iso3_code", "pop_density", "emission_factor"],
            'col_dtypes': ["string", "float64", "float64"]
        },

        'heating_demand_data': {
            'extension': '.csv',
            'original_cols': ["Climate zone", "[GWh/(m2,a)]"],
            'renamed_cols': ["climate_zone", "heating_demand_factor"],
            'col_dtypes': ["int64", "float64"]
        },

        'manual_continents_data': {
            'extension': '.csv',
            'original_cols': ["Alpha-3 code", "Closest continent"],
            'renamed_cols': ["iso3_code", "continent_name"],
            'col_dtypes': ["string", "string"]
        },

        'ne_countries_continents': {
            'extension': '.csv',
            'original_cols': ["CONTINENT", "ADM0_A3"],
            'renamed_cols': ["continent_name", "iso3_code"],
            'col_dtypes': ["string", "string"]
        },
        'on_site_heat_data': {
            'extension': '.csv',
            'original_cols': ["Continent", "On-site heating energy generation factors", " Heated floor area factors", "on-site heated floor area factor"],
            'renamed_cols': ["continent_name", "oheg_factor", "hfa_factor", "ohfa_factor"],
            'col_dtypes': ["string", "float64", "float64", "float64"]
        }
    }


    ds_names = list(schema.keys())

    def __init__(self, data_dir):
        self.dir = data_dir

    def read_and_parse(self, v=True, q=False):
        if q:
            v = False
        ds_exts = [self.schema[key]['extension'] for key in self.ds_names]
        datasets = r.read_datasets(self.dir, self.ds_names, ds_exts)
        parsed_datasets = {}

        for key in self.ds_names:
            original_cols = self.schema[key]['original_cols']
            renamed_cols = self.schema[key]['renamed_cols']
            col_dtypes = self.schema[key]['col_dtypes']
            not q and print('Dataset: {}'.format(key))
            parsed_datasets[key] = r.parse_datasets(
                original_cols, renamed_cols, col_dtypes, datasets[key], v=v)
            not q and print('{}\n***\n'.format(parsed_datasets[key].shape))

        return parsed_datasets


