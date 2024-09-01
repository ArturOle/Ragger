import pytest

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
