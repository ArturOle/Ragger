import os
import logging

from ragger.data_manager.reader import PDFReader

cur_dir = os.path.dirname(__file__)
logger = logging.getLogger(__name__)


def test_pdf_reader_read():
    logger.info(cur_dir)
    text = PDFReader().read(
        rf'{cur_dir}/test_files/test.pdf'
    )
    assert text == 'Test\ntseT\n'


def test_pdf_reader_scanned_read():
    logger.info(cur_dir)
    text = PDFReader().read(
        rf'{cur_dir}/test_files/test_scanned.pdf',
    )
    assert "Test\ntseT" in text
