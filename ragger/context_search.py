from . import data_manager


class ContextSearch:
    """Facade class for the data_manager module."""
    def __init__(self):
        self.data_manager = data_manager.DataManager()

    def submit(self, path):
        self.data_manager.insert(path)

    def retrive(self, query, n=1):
        return self.data_manager.retrieve_data(query, n)
