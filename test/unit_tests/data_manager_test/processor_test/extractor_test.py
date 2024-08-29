
from ragger.data_manager.processor.extractor import Extractor


def test_extractor_extract_keywords():
    correct_ranks = [
        "a test text 0.25",
        "This 0.0"
    ]
    extractor = Extractor()
    text = "This is a test text. This is a test text. This is a test text."
    ranks = extractor.extract_keywords(text)

    for i, rank in enumerate(ranks):
        assert ' '.join((str(r) for r in rank)) == correct_ranks[i]
        assert len(rank) == 2
