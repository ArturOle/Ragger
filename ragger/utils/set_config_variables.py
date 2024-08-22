
import os


def get_config_variables():
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


def set_env_variables_from_config():
    tesseract_path, poppler_path = get_config_variables()
    os.environ["TESSERACT_PATH"] = tesseract_path
    os.environ["POPPLER_PATH"] = poppler_path
