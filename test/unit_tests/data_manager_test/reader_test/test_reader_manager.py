import os
import pytest

from ragger.data_manager.reader import ReaderManager
from ragger.data_managerdata_classes import LiteratureDTO

cur_dir = os.path.dirname(__file__)


def test_reader_manager_read_pdf(mocker):
    reader_manager = ReaderManager()

    mock_pdf_reader = mocker.patch.object(reader_manager.pdf_reader, 'read')
    mock_pdf_reader.return_value = "test"
    mock_text_reader = mocker.patch.object(reader_manager.text_reader, 'read')
    mock_text_reader.return_value = "test"

    result = reader_manager.read(f"{cur_dir}/test_files/test.txt")
    mock_pdf_reader.assert_called_once()
    assert isinstance(result, list) and len(result) == 1

    result = reader_manager.read(f"{cur_dir}/test_files/test.pdf")
    mock_pdf_reader.assert_not_called()
    assert isinstance(result, list) and len(result) == 1

    result = reader_manager.read(f"{cur_dir}/test_files")
    assert isinstance(result, list) and len(result) == 1

    assert_n_calls(mock_pdf_reader, 3)


def test_reader_manager_read_txt(mocker):
    reader_manager = ReaderManager()

    mock_text_reader = mocker.patch.object(reader_manager.text_reader, 'read')
    mocker.patch.object(reader_manager.pdf_reader, 'read')

    result = reader_manager.read(f"{cur_dir}/test_files/test.pdf")
    mock_text_reader.assert_not_called()
    assert isinstance(result, list) and len(result) == 1

    result = reader_manager.read(f"{cur_dir}/test_files/test.txt")
    mock_text_reader.assert_called_once()
    assert isinstance(result, list) and len(result) == 1

    result = reader_manager.read(f"{cur_dir}/test_files")
    assert isinstance(result, list) and len(result) == 1

    assert_n_calls(mock_text_reader, 2)


def assert_n_calls(mock, n):
    assert mock.call_count == n