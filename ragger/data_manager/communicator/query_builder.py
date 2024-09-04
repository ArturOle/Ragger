from ..data_classes import (
    LiteratureGraph,
    Literature,
    Chunk,
    Tag,
    RelationWeight
)
from collections import OrderedDict


class QueryBuilder:

    @staticmethod
    def expand_parameters(parameters: dict):
        return ", ".join([f"{key}: ${key}" for key in parameters.keys()])

    @staticmethod
    def add_literature_subgraph(literature_graph: LiteratureGraph):
        queries = OrderedDict()

        queries[literature_graph.literature] = QueryBuilder.add_literature(
            literature_graph.literature
        )

        for chunk in literature_graph.chunks:
            queries[chunk] = (
                QueryBuilder.add_chunk(chunk),
                QueryBuilder.add_relation_literature_chunk()
            )

        for tag in literature_graph.tags:
            queries[tag] = (
                QueryBuilder.add_tag(tag),
                QueryBuilder.add_relation_literature_tag()
            )

        return queries

    @staticmethod
    def find_literature_by_filename():
        return "MATCH (l:Literature) WHERE l.filename = $literature_filename"

    @staticmethod
    def add_relation_literature_chunk():
        return "MERGE (l)<-[:PART_OF]-(c)"

    @staticmethod
    def add_literature(literature: Literature):
        params = QueryBuilder.expand_parameters(literature.model_fields)
        return f"MERGE (l:Literature {{{params}}})"

    @staticmethod
    def add_chunk(chunk: Chunk):
        params = QueryBuilder.expand_parameters(chunk.model_fields)
        return f"MERGE (c:Chunk {{{params}}})"

    @staticmethod
    def add_tag(tag: Tag):
        params = QueryBuilder.expand_parameters(tag.model_fields)
        return f"MERGE (t:Tag{{{params}}})"

    @staticmethod
    def add_relation_literature_tag():
        return "MERGE (l)-[:RELATED_TO{weight: $weight}]->(t)"
