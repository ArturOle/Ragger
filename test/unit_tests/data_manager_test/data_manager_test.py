from ragger.data_manager import DataManager


class FakeCommunicator:
    def __init__(self, uri, user, password):
        pass

    def add_literature_subgraph(self, literature):
        pass

    def create_vector_indexes(self):
        pass

    def search_n_records(self, query, n):
        pass


def test_insert(mocker):
    data_manager = DataManager()
    data_manager._communicator = mocker.MagicMock(spec=FakeCommunicator)

    read_mock = mocker.patch.object(data_manager.read_manager, 'read')
    read_mock.return_value = ['Totally not mocked literature object']

    preprocessor_mock = mocker.patch.object(data_manager.preprocessor, 'process')
    preprocessor_mock.return_value = ['Totally not mocked literature object, but processed']

    data_manager.insert([
        'test/unit_tests/data_manager_test/test_data/pdf-ai-generated/ML_article.pdf'
    ])

    assert data_manager.communicator.add_literature_subgraph.call_count == 1
    assert data_manager.communicator.create_vector_indexes.call_count == 1
    assert read_mock.call_count == 1
    assert preprocessor_mock.call_count == 1


def test_retrieve(mocker):
    data_manager = DataManager()
    data_manager._communicator = mocker.MagicMock(spec=FakeCommunicator)

    search_mock = mocker.patch.object(data_manager.communicator, 'search_n_records')
    embedder_mock = mocker.patch.object(data_manager.preprocessor.embedder, 'embed')

    data_manager.retrieve_data('test', 1)

    assert search_mock.call_count == 1
    assert embedder_mock.call_count == 1


def communicator_property_test(mocker):
    data_manager = DataManager()

    variable_fetch_mock = mocker.patch('ragger.data_manager.manager.config_variables.get_neo4j_variables')
    variable_fetch_mock.return_value = ['uri', 'user', 'password']
    communicator_mock = mocker.patch('ragger.data_manager.manager.Communicator')

    data_manager.communicator

    assert communicator_mock.call_count == 1
