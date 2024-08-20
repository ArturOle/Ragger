import os
import logging

from ragger.data_manager import TextReader

cur_dir = os.path.dirname(__file__)
logger = logging.getLogger(__name__)


def test_text_reader_read():

    text_reader = TextReader(
        rf'{cur_dir}\test_files\test.txt',
        False
    )
    assert text_reader.read() == 'Test\ntseT'
