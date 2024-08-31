from ragger.data_manager import DataManager


def test_insert(mocker):
    data_manager = DataManager()
    mocker.patch.object(data_manager.communicator, 'add_literature')
    data_manager.insert(['test/unit_tests/data_manager_test/test_data/pdf-ai-generated/ML_article.pdf'])
