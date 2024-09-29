from . import data_manager


class ContextSearch:
    def __init__(self):
        self.data_manager = data_manager.DataManager()

    def submit(self, path):
        self.data_manager.insert(path)

    def retrive(self, query):
        return self.data_manager.retrieve_data(query, 5)
