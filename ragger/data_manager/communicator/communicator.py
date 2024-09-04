from neo4j import GraphDatabase
from ..utils import setup_logger
from ..data_classes import (
    Literature, Chunk, Tag, RelationWeight, LiteratureGraph
)

logger = setup_logger("Communicator Logger", "logs.log")


# TODO: Descripion: This class is WAY too big. It would be useful to split it
# into smaller classes. Task: Split the Communicator class into smaller classes.
# Tags: refactor
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
        self._merge_literature(tx, literature_graph.literature)

        for chunk in literature_graph.chunks:
            self._merge_chunk(tx, chunk)
            self._connect_chunk(tx, chunk, literature_graph.literature)

        for tag in literature_graph.tags:
            self._merge_tag(tx, tag)
            self._connect_tag(tx, tag, literature_graph.literature)

        for relation_weight in literature_graph.relation_weights:
            self._merge_relation_weight(tx, relation_weight)

    def _merge_literature(self, tx, literature: Literature):
        tx.run(
            "MERGE (l:Literature {filename: $filename, filepath: $filepath})",
            filename=literature.filename,
            filepath=literature.filepath
        )

    def _merge_chunk(self, tx, chunk: Chunk):
        tx.run(
            "MERGE (c:Chunk {text: $text})",
            text=chunk.text
        )

    def _connect_chunk(self, tx, chunk: Chunk, literature: Literature):
        tx.run(
            "MATCH (l:Literature {filename: $filename}) "
            "MATCH (c:Chunk {text: $text}) "
            "MERGE (l)<-[:PART_OF]-(c)",
            filename=literature.filename,
            text=chunk.text
        )

    def _merge_tag(self, tx, tag: Tag):
        tx.run(
            "MERGE (t:Tag {text: $text})",
            text=tag.text
        )

    def _connect_tag(self, tx, tag: Tag, literature: Literature):
        tx.run(
            "MATCH (l:Literature {filename: $filename}) "
            "MATCH (t:Tag {text: $text}) "
            "MERGE (l)-[:TAGGED]->(t)",
            filename=literature.filename,
            text=tag.text
        )

    def _merge_relation_weight(self, tx, relation_weight: RelationWeight):
        tx.run(
            "MATCH (l:Literature {filename: $literature}) "
            "MATCH (t:Tag {text: $tag}) "
            "MERGE (l)-[:RELATED_TO {weight: $weight}]->(t)",
            literature=relation_weight.literature,
            tag=relation_weight.tag,
            weight=relation_weight.weight
        )

    @connection
    def get_literature(self, session, filename):
        return session.read_transaction(self._get_literature, filename)

    def _get_literature(self, tx, filename):
        try:
            retieved_document = tx.run(
                "MATCH (l:Literature) WHERE l.filename = $filename RETURN l",
                filename=filename
            ).single()[0]
            logger.info(f"Literature {retieved_document} found.")
            return retieved_document
        except TypeError:
            logger.info("No literatures found.")
            return None

    @connection
    def get_literature_chunks(self, session, filename):
        return session.read_transaction(self._get_literature_chunks, filename)

    def _get_literature_chunks(self, tx, filename):
        try:
            return [record[0] for record in tx.run(
                "MATCH (l:Literature {filename: $filename})<-[:PART_OF]-(c:Chunk) RETURN c",
                filename=filename
            )]
        except TypeError:
            logger.info("No chunks found.")
            return []

    @connection
    def get_literature_tags(self, session, filename):
        return session.read_transaction(self._get_literature_tags, filename)

    def _get_literature_tags(self, tx, filename):
        try:
            return [record[0] for record in tx.run(
                "MATCH (l:Literature {filename: $filename})-[:TAGGED]->(t:Tag) RETURN t",
                filename=filename
            )]
        except TypeError:
            logger.info("No tags found.")
            return []

    @connection
    def get_all_literatures(self, session):
        return session.read_transaction(self._get_all_literatures)

    def _get_all_literatures(self, tx):
        try:
            return [record[0] for record in tx.run(
                "MATCH (l:Literature) RETURN l"
            )]
        except TypeError:
            logger.info("No literatures found.")
            return []

    # @connection
    # def add_literature(self, session, literature: Literature):
    #     session.write_transaction(self._add_literature, literature)

    # def _add_literature(self, tx, literature: Literature):
    #     return tx.run(
    #         "MERGE (l:Literature {filename: $filename, filepath: $filepath})",
    #         filename=literature.filename,
    #         filepath=literature.filepath
    #     )

    @connection
    def delete_literature(self, session, filename):
        session.write_transaction(self._delete_literature, filename)

    def _delete_literature(self, tx, filename):
        return NotImplementedError
        # return tx.run(
        #     "MATCH (a:Literature) WHERE a.filename = $filename DELETE a",
        #     filename=filename
        # )
