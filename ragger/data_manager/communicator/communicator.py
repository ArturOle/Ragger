from neo4j import GraphDatabase
from ..utils import setup_logger
from ..data_classes import LiteratureGraph
from .query_builder import QueryBuilder


logger = setup_logger("Communicator Logger", "logs.log")


class Communicator:
    """Communicator class for interacting with the Neo4j database.

    Attributes:
        uri (str): The URI of the Neo4j database.
        user (str): The username for the Neo4j database.
        password (str): The password for the Neo4j database.
    """

    def __init__(self, uri, user, password):
        self._uri = uri
        self._user = user
        self._password = password
        self._driver = None

    @property
    def driver(self):
        if self._driver is None:
            self._driver = GraphDatabase.driver(
                self._uri,
                auth=(self._user, self._password)
            )
        return self._driver

    @driver.setter
    def driver(self, driver):
        self._driver = driver

    @driver.deleter
    def driver(self):
        if self._driver is not None:
            self._driver.close()
        del self._driver

    @staticmethod
    def connection(func):
        def wrapper(self, *args, **kwargs):
            session = self.driver.session(database="neo4j")
            result = func(self, session, *args, **kwargs)
            session.close()
            return result

        return wrapper

    # TODO: Descripion: It would be useful to create a wrapper function for
    # query profiling. Task: Create a wrapper function for query profiling.
    # Tags: feature, monitoring

    @connection
    def add_literature_subgraph(
            self,
            session,
            literature_graph: LiteratureGraph
    ):
        session.write_transaction(
            self._add_literature_subgraph,
            literature_graph
        )

    @connection
    def create_vector_indexes(self, session):
        """Creates vector indexes for chunks and tags.
        This function is separated from the add_literature_subgraph
        because the indexes cannot be created in the same transaction"""
        session.write_transaction(self._index_ebeddables)

    def _add_literature_subgraph(self, tx, literature_graph: LiteratureGraph):
        """Builds the the nodes and relationships based on the given
        LiteratureGraph object. All elements are merged with existing
        graph elements."""
        QueryBuilder._merge_literature(tx, literature_graph.literature)

        for chunk in literature_graph.chunks:
            QueryBuilder._merge_chunk(tx, chunk)
            QueryBuilder._connect_chunk(tx, chunk, literature_graph.literature)

        for tag in literature_graph.tags:
            QueryBuilder._merge_tag(tx, tag)
            QueryBuilder._connect_tag(tx, tag, literature_graph.literature)

        for relation_weight in literature_graph.relation_weights:
            QueryBuilder._merge_relation_weight(tx, relation_weight)

    def _index_ebeddables(self, tx):
        QueryBuilder._index_chunks(tx)
        QueryBuilder._index_tags(tx)

    @connection
    def get_literature(self, session, filename):
        return session.read_transaction(QueryBuilder._get_literature, filename)

    @connection
    def get_literature_chunks(self, session, filename):
        return session.read_transaction(
            QueryBuilder._get_literature_chunks,
            filename
        )

    @connection
    def get_literature_tags(self, session, filename):
        return session.read_transaction(
            QueryBuilder._get_literature_tags,
            filename
        )

    @connection
    def search_n_records(self, session, query, n):
        return session.read_transaction(
            QueryBuilder._search_n_records,
            query,
            n
        )

    @connection
    def get_all_literatures(self, session):
        return session.read_transaction(QueryBuilder._get_all_literatures)

    @connection
    def delete_literature(self, session, filename):
        session.write_transaction(QueryBuilder._delete_literature, filename)

    def __del__(self):
        if self._driver is not None:
            self._driver.close()
            logger.info("Driver closed")
