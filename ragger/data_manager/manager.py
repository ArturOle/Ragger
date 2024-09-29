import os

from .reader import ReadManager
from .preprocessor import Preprocessor
from .communicator import Communicator
from .utils import setup_logger, config_variables


logger = setup_logger('Data Manager Logger', 'logs.log')


class DataManager:
    """Class for handling the data flow, sets up necessary components and
    provides methods for inserting and retrieving data."""
    _communicator = None

    def __init__(self):
        self.read_manager = ReadManager()
        self.preprocessor = Preprocessor()

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

    @communicator.setter
    def communicator(self, communicator):
        self._communicator = communicator

    def retrieve_data(self, query, n):
        """Retrieves n records from the database based on the query.

        Parameters:
            query (str): The question asked by the user.
            n (int): The number of the most similar records.

        Returns:
            list: A list of n most similar records together with
            similarity score.
        """
        embedded_query = self.preprocessor.embedder.embed(query)
        return self.communicator.search_n_records(embedded_query, n)

    def insert(self, directories: list) -> None:
        """Inserts data from the given directories to the database.

        Parameters:
            directories (list): A list of directories containing the data.
        """
        literatures = []
        for directory in directories:
            if os.path.exists(directory):
                literatures.extend(self.read_manager.read(directory))
            else:
                logger.error(f"Directory {directory} does not exist.")

        if literatures.__len__() == 0:
            logger.error(
                f"No literatures found in directories {directories}."
                " Current directory {os.getcwd()}"
            )
            raise FileNotFoundError(
                f"No literatures found in directories {directories}."
            )

        literatures = self.preprocessor.process(literatures)

        for literature in literatures:
            self.communicator.add_literature_subgraph(literature)
            self.communicator.create_vector_indexes()
