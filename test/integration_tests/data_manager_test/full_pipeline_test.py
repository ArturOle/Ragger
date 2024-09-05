import pytest
import os

from ragger.data_manager import DataManager

cwd = os.getcwd()


class TestFillingDatabase:
    def setup_test(test):
        test.data_manager = DataManager()

    def test_insert_single_file(test):
        test.setup_test()
        test.data_manager.insert(
            [cwd + r"/test/integration_tests/data_manager_test/test_data/pdf-ai-generated/ES_article.pdf"]
        )
        assert test.data_manager.communicator.get_literature("ES_article.pdf") is not None

    def test_insert_multiple_files(test):
        test.setup_test()
        test.data_manager.insert(
            [cwd + r"/test/integration_tests/data_manager_test/test_data/pdf-ai-generated/ES_article.pdf",
             cwd + r"/test/integration_tests/data_manager_test/test_data/pdf-ai-generated/ML_article.pdf"]
        )
        assert test.data_manager.communicator.get_literature("ES_article.pdf") is not None
        assert test.data_manager.communicator.get_literature("ML_article.pdf") is not None
