import json
import sys, os
sys.path.append(os.path.abspath(os.path.join('..', 'modules')))

import read as r

class Ingest:
    '''Ingests all input data needed for the project.
    
    Class members
    -------------
    schema: object holding information to parse input datasets
    ds_names: list of input datasets
    '''

    def __init__(self, schema_file):
        '''
        Params
        ------
        schema_file: string, relative or absolute path of schema file (json)
        '''
        with open(schema_file, mode='r') as f:
            self.schema = json.load(f)

        self.ds_names = list(self.schema.keys())

    def read_and_parse(self, data_dir, v=True, q=False):
        '''
        Params
        ------
        data_dir: string, relative or absolute path for input data
        v: boolean, toggel verbosity, default True
        q: boolean: toggel quiet, default False (if true, v is automatically false)

        Returns
        -------
        parsed_datasets: Dictionary with dataset names as keys and dataframes as values
        '''
      
        if q:
            v = False
        ds_exts = [self.schema[key]['extension'] for key in self.ds_names]
        datasets = r.read_datasets(data_dir, self.ds_names, ds_exts)
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


