from ragger.data_manager.reader import FileTypeRecon


def test_is_directory_or_file_dir():
    assert FileTypeRecon.is_directory_or_file("./test") is True


def test_is_directory_or_file_file():
    assert FileTypeRecon.is_directory_or_file("./README.md") is False


def test_recognize_type_valid():
    assert FileTypeRecon.recognize_type("a.pdf") == "pdf"
    assert FileTypeRecon.recognize_type("a.txt") == "txt"


def test_recognize_type_invalid(caplog):
    FileTypeRecon.recognize_type("a.jpg")
    assert caplog.records[-1].levelname == "WARNING"
    assert caplog.records[-1].message == (
        "Unsupported file type. The file a.jpg will be skipped."
        "Please provide a file of the following types: txt, pdf"
    )
