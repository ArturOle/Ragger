import os
from context_search.reader import TextReader

cur_dir = os.path.dirname(__file__)


def test_text_reader_read():

    text = TextReader.read(
        rf'{cur_dir}/test_files/test.txt',
    )
    assert text == ['Test\ntseT']
