
import os


def get_OCR_variables():
    tesseract_path = ""
    poppler_path = ""

    current_working_directory = os.getcwd()
    path_to_config = os.path.join(current_working_directory, "config.ini")
    with open(path_to_config, "r") as file:
        lines = file.readlines()

        for line in lines:
            if line.startswith("TESSERACT_PATH"):
                tesseract_path = line.split("=")[1].strip()
            if line.startswith("POPPLER_PATH"):
                poppler_path = line.split("=")[1].strip()

    return tesseract_path, poppler_path


def get_neo4j_variables():
    uri = ""
    user = ""
    password = ""

    current_working_directory = os.getcwd()
    path_to_config = os.path.join(current_working_directory, "config.ini")
    with open(path_to_config, "r") as file:
        lines = file.readlines()

        for line in lines:
            if line.startswith("NEO4J_URI"):
                uri = line.split("=")[1].strip()
            if line.startswith("NEO4J_USER"):
                user = line.split("=")[1].strip()
            if line.startswith("NEO4J_PASSWORD"):
                password = line.split("=")[1].strip()

    return uri, user, password


def set_env_variables_from_config():
    tesseract_path, poppler_path = get_OCR_variables()
    os.environ["TESSERACT_PATH"] = tesseract_path
    os.environ["POPPLER_PATH"] = poppler_path

    uri, user, password = get_neo4j_variables()
    os.environ["NEO4J_URI"] = uri
    os.environ["NEO4J_USER"] = user
    os.environ["NEO4J_PASSWORD"] = password
