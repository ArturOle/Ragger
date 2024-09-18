from neo4j import GraphDatabase
from ..utils import setup_logger
from ..data_classes import LiteratureGraph
from .query_builder import QueryBuilder


logger = setup_logger("Communicator Logger", "logs.log")


class Communicator:
    """ Communicator class for interacting with the Neo4j database.

    Why there is so much redundancy in queries? On purpouse.
    It makes the operations more atomic, assure that the queries are
    independent and if session is closed between individual queries, there will
    be in future log-based stop points that will finish queries.
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

    def _add_literature_subgraph(self, tx, literature_graph: LiteratureGraph):
        QueryBuilder._merge_literature(tx, literature_graph.literature)

        for chunk in literature_graph.chunks:
            QueryBuilder._merge_chunk(tx, chunk)
            QueryBuilder._connect_chunk(tx, chunk, literature_graph.literature)

        for tag in literature_graph.tags:
            QueryBuilder._merge_tag(tx, tag)
            QueryBuilder._connect_tag(tx, tag, literature_graph.literature)

        for relation_weight in literature_graph.relation_weights:
            QueryBuilder._merge_relation_weight(tx, relation_weight)

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
    def get_all_literatures(self, session):
        return session.read_transaction(QueryBuilder._get_all_literatures)

    @connection
    def delete_literature(self, session, filename):
        session.write_transaction(QueryBuilder._delete_literature, filename)

    def __del__(self):
        if self._driver is not None:
            self._driver.close()
            logger.info("Driver closed")
