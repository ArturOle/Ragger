import pytest

from data_manager.communication import Communicator
from data_manager.data_classes import Literature


class TestCommunicatorConnection:
    def setup_test(test):
        test.uri = "neo4j://localhost:7687"
        test.user = "neo4j"
        test.password = "StrongPsPsP5"
        test.communicator = None

    def test_communicator_creation(test):
        test.setup_test()
        test.communicator = Communicator(test.uri, test.user, test.password)
        assert test.communicator is not None


class TestCommunicatorTransactions:
    @pytest.mark.dependency(
        depends=["TestCommunicatorConnection::test_communicator_creation"])
    def setup_test(test):
        test.uri = "neo4j://localhost:7687"
        test.user = "neo4j"
        test.password = "StrongPsPsP5"
        test.communicator = Communicator(test.uri, test.user, test.password)
        test.literature = Literature(
            filename="test",
            text="This is a test text.",
            text_position=0,
            page_number=0
        )

    @pytest.mark.dependency(
        depends=["TestCommunicatorConnection::test_communicator_creation"])
    def test_add_literature(test):
        test.setup_test()
        test.communicator.add_literature(test.literature)

    @pytest.mark.dependency(depends=["test_add_literature"])
    def test_get_literature(test):
        test.setup_test()
        test.communicator.add_literature(test.literature)
        literature = test.communicator.get_literature("test")
        print(literature)
        assert literature is not None

    @pytest.mark.dependency(depends=["test_add_literature"])
    def test_get_all_literatures(test):
        test.setup_test()
        test.communicator.add_literature(test.literature)
        literatures = test.communicator.get_all_literatures()
        assert len(literatures) > 0

    @pytest.mark.dependency(depends=["test_add_literature"])
    def test_delete_literature(test):
        test.setup_test()
        test.communicator.add_literature(test.literature)
        test.communicator.delete_literature("test")
        assert test.communicator.get_literature("test") is None
