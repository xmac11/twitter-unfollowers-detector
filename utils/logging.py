import logging
import os

from settings import LOGS_ROOT


def setup_logger(*, name, level, filename):
    logger = logging.getLogger(name)
    logger.setLevel(level)

    file_handler = logging.FileHandler(os.path.join(LOGS_ROOT, filename))
    file_formatter = logging.Formatter('%(asctime)s %(name)s %(levelname)s %(message)s', '%d-%m-%Y %H:%M:%S')
    file_handler.setFormatter(file_formatter)

    stream_handler = logging.StreamHandler()
    stream_formatter = logging.Formatter('%(message)s')
    stream_handler.setFormatter(stream_formatter)

    logger.addHandler(file_handler)
    logger.addHandler(stream_handler)

    return logger
