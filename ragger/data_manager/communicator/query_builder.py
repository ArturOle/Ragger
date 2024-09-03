from ragger.data_manager.data_classes import (
    LiteratureGraph,
    Literature,
    Chunk,
    Tag,
    RelationWeight
)


class QueryBuilder:

    @staticmethod
    def add_literature_subgraph(literature_graph: LiteratureGraph):
        pass

    @staticmethod
    def add_relation_literature_chunk(
            literature: Literature, chunk: Chunk
    ):
        return (
            f"MATCH (l:Literature) WHERE l.filename = '{literature.filename}'",
            f"MATCH (c:Chunk) WHERE c.text = '{chunk.text}'",
            "MERGE (l)<-[:PART_OF]-(c)"
        )

    @staticmethod
    def add_literature(literature: Literature):
        return f"MERGE (a:Literature {{{literature.to_dict()}}})"

    @staticmethod
    def add_chunk(chunk: Chunk):
        return f"MERGE (a:Chunk {{{chunk.to_dict()}}})"

    @staticmethod
    def add_tag(tag: Tag):
        return f"MERGE (a:Tag{{{tag.to_dict()}}})"

    @staticmethod
    def add_relation_literature_tag(
            literature: Literature, tag: Tag, RelationWeight: RelationWeight
    ):
        return (
            f"MATCH (l:Literature) WHERE l.filename = '{literature.filename}'",
            f"MATCH (t:Tag) WHERE t.text = '{tag.text}'",
            f"MERGE (l)-[:RELATED_TO{{{RelationWeight.weight}}}]->(t)"
        )
