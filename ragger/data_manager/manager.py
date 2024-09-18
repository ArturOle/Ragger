import os

from .reader import ReadManager
from .preprocessor import Preprocessor
from .communicator import Communicator
from .utils import setup_logger, config_variables


logger = setup_logger('Data Manager Logger', 'logs.log')


class DataManager:
    _communicator = None

    def __init__(self):
        self.read_manager = ReadManager()
        self.process_manager = Preprocessor()

    @property
    def communicator(self):
        if self._communicator is None:
            neo4j_variables = config_variables.get_neo4j_variables()
            self._communicator = Communicator(
                uri=neo4j_variables[0],
                user=neo4j_variables[1],
                password=neo4j_variables[2]
            )
            logger.info(f"""
            Communicator created with:
            uri: {neo4j_variables[0]}
            user: {neo4j_variables[1]}
            password: {neo4j_variables[2]}
            """)
        return self._communicator

    def retrive_data(self):
        return self.communicator.get_all_literatures()

    def insert(self, directories):
        literatures = []
        for directory in directories:
            if os.path.exists(directory):
                literatures.extend(self.read_manager.read(directory))
            else:
                logger.error(f"Directory {directory} does not exist.")

        if literatures.__len__() == 0:
            logger.error(f"No literatures found in directories {directories}. Current directory {os.getcwd()}")
            raise FileNotFoundError(
                f"No literatures found in directories {directories}."
            )

        literatures = self.process_manager.process(literatures)

        for literature in literatures:
            self.communicator.add_literature_subgraph(literature)
