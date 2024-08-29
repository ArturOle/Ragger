import pytest
from ragger.data_manager.reader import FileTypeRecon


def test_is_directory_or_file_dir():
    assert FileTypeRecon.is_directory_or_file("./test") is True


def test_is_directory_or_file_file():
    assert FileTypeRecon.is_directory_or_file("./dockerfile") is False


def test_recognize_type_valid():
    assert FileTypeRecon.recognize_type("a.pdf") == "pdf"
    assert FileTypeRecon.recognize_type("a.txt") == "txt"


def test_recognize_type_invalid():
    with pytest.raises(ValueError, match="Unsupported file type"):
        FileTypeRecon.recognize_type("a.jpg")
