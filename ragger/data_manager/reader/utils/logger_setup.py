import logging


def setup_logger(name, log_file, level=logging.INFO):
    logging_level = level

    logger = logging.getLogger('Reader Logger')
    logger.setLevel(logging_level)

    file_handler = logging.FileHandler('logs.log')
    console_handler = logging.StreamHandler()

    file_handler.setLevel(logging_level)
    console_handler.setLevel(logging_level)

    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger
