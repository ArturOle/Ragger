from ragger.data_manager import DataManager


# TODO: Description: This test does not test anything.
# Task: Write a meaningful test that tests the DataManager class.
# Tags: tests
def test_insert(mocker):
    data_manager = DataManager()
    mocker.patch.object(data_manager.communicator, 'add_literature_subgraph')
    data_manager.insert([
        'test/unit_tests/data_manager_test/test_data/pdf-ai-generated/ML_article.pdf'
    ])
