import os
import logging

from ragger.data_manager.reader import TextReader

cur_dir = os.path.dirname(__file__)
logger = logging.getLogger(__name__)


def test_text_reader_read():

    text = TextReader.read(
        rf'{cur_dir}/test_files/test.txt',
    )
    assert text == 'Test\ntseT'
