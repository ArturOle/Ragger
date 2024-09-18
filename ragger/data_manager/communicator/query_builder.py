from ..data_classes import (
    Literature,
    Chunk,
    Tag,
    RelationWeight
)

from ..utils import setup_logger
logger = setup_logger("Communicator Logger", "logs.log")


class QueryBuilder:

    @staticmethod
    def get_literature(tx, filename):
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

    @staticmethod
    def _merge_literature(tx, literature: Literature):
        tx.run(
            "MERGE (l:Literature {filename: $filename, filepath: $filepath})",
            filename=literature.filename,
            filepath=literature.filepath
        )

    @staticmethod
    def _merge_chunk(tx, chunk: Chunk):
        tx.run(
            "MERGE (c:Chunk {text: $text})",
            text=chunk.text
        )

    @staticmethod
    def _connect_chunk(tx, chunk: Chunk, literature: Literature):
        tx.run(
            "MATCH (l:Literature {filename: $filename}) "
            "MATCH (c:Chunk {text: $text}) "
            "MERGE (l)<-[:PART_OF]-(c)",
            filename=literature.filename,
            text=chunk.text
        )

    @staticmethod
    def _merge_tag(tx, tag: Tag):
        tx.run(
            "MERGE (t:Tag {text: $text})",
            text=tag.text
        )

    @staticmethod
    def _connect_tag(tx, tag: Tag, literature: Literature):
        tx.run(
            "MATCH (l:Literature {filename: $filename}) "
            "MATCH (t:Tag {text: $text}) "
            "MERGE (l)-[:TAGGED]->(t)",
            filename=literature.filename,
            text=tag.text
        )

    @staticmethod
    def _merge_relation_weight(tx, relation_weight: RelationWeight):
        tx.run(
            "MATCH (l:Literature {filename: $literature}) "
            "MATCH (t:Tag {text: $tag}) "
            "MERGE (l)-[:RELATED_TO {weight: $weight}]->(t)",
            literature=relation_weight.literature,
            tag=relation_weight.tag,
            weight=relation_weight.weight
        )

    @staticmethod
    def _get_literature(tx, filename):
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

    @staticmethod
    def _get_literature_chunks(tx, filename):
        try:
            return [record[0] for record in tx.run(
                "MATCH (l:Literature {filename: $filename})<-[:PART_OF]-(c:Chunk) RETURN c",
                filename=filename
            )]
        except TypeError:
            logger.info("No chunks found.")
            return []

    @staticmethod
    def _get_literature_tags(tx, filename):
        try:
            return [record[0] for record in tx.run(
                "MATCH (l:Literature {filename: $filename})-[:TAGGED]->(t:Tag) RETURN t",
                filename=filename
            )]
        except TypeError:
            logger.info("No tags found.")
            return []

    @staticmethod
    def _get_all_literatures(tx):
        try:
            return [record[0] for record in tx.run(
                "MATCH (l:Literature) RETURN l"
            )]
        except TypeError:
            logger.info("No literatures found.")
            return []

    @staticmethod
    def _delete_literature(tx, filename):
        return NotImplementedError
        # return tx.run(
        #     "MATCH (a:Literature) WHERE a.filename = $filename DELETE a",
        #     filename=filename
        # )
