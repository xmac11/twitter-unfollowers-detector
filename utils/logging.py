import logging
import os

from constants.logs import FORMAT, DATE_FORMAT
from settings import LOGS_ROOT


def setup_logger(*, name, level, filename):
    logger = logging.getLogger(name)
    logger.setLevel(level)

    file_handler = logging.FileHandler(os.path.join(LOGS_ROOT, filename))

    formatter = logging.Formatter(FORMAT, DATE_FORMAT)
    file_handler.setFormatter(formatter)

    logger.addHandler(file_handler)

    return logger
