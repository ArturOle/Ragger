import os

from .reader import ReadManager
from .processor import ProcessorManager


class DataManager:
    def __init__(self):
        # self.db_manager = DBManager()
        self.read_manager = ReadManager()
        self.process_manager = ProcessorManager()

    def retrive_data(self):
        return self.communicator.get_all_literatures()

    def insert(self, directories):
        literatures = []
        for directory in directories:
            if os.path.exists(directory):
                literatures.extend(self.read_manager.read(directory))

        literatures = self.process_manager.process(literatures)
        # self.db_manager.insert(literatures)


if __name__ == '__main__':
    data_manager = DataManager()
