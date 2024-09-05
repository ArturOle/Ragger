import pytest

from unittest.mock import MagicMock, patch

from ragger.data_manager.communicator import Communicator


class TestCommunicatorConnection:
    def setup_test(test):
        test.uri = "neo4j://database:7687"
        test.user = "neo4j"
        test.password = "StrongPsPsP5"
        test.communicator = None

    def test_communicator_creation(test):
        test.setup_test()
        test.communicator = Communicator(test.uri, test.user, test.password)
        assert test.communicator is not None
        test.communicator = None


@pytest.fixture
def mock_driver():
    with patch("neo4j.GraphDatabase.driver") as mock_driver:
        yield mock_driver


class TestInterfaceInvocations:
    def setup_test(test):
        test.uri = "neo4j://database:7687"
        test.user = "neo4j"
        test.password = "StrongPsPsP5"
        test.communicator = Communicator(test.uri, test.user, test.password)

    def test_driver_property_invocation(test, mock_driver):
        test.setup_test()
        mock_session = MagicMock()
        mock_driver.return_value.session.return_value\
            .__enter__.return_value = mock_session
        mock_driver.return_value.session.read_transaction = MagicMock()
        mock_driver.return_value.session.close = MagicMock()

        test.communicator.get_literature("test_file")

        mock_driver.assert_called_once_with(
            test.uri, auth=(test.user, test.password)
        )
        mock_driver.return_value.session.assert_called_once_with(database="neo4j")
