import pytest
import glob
import sys, os

sys.path.append(os.path.abspath(os.path.join('..', '..', 'src')))
import ingest.ingest as ing

class TestIngest:

    @pytest.fixture
    def data_dir(self):
        return os.path.abspath(os.path.join('..', 'ingest', 'data_in')) + '/'

    @pytest.fixture
    def schema_file(self):
        return os.path.abspath(os.path.join('..', 'ingest')) + '/schema.json'

    def test_all_data_read(self, data_dir, schema_file):
        pattern = '*.csv'
        imatches = glob.iglob(data_dir + '/' + pattern)
        file_count = len([match for match in imatches])
        ingest = ing.Ingest(schema_file)
        result = ingest.read_and_parse(data_dir)
        assert len(result) == file_count
