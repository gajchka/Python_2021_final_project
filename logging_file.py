"""
Module contains function that defines logger with its handlers and formatters
"""
import logging


def define_logger():
    """
    Creates logger, connects it with handlers and defines format of log messages.
    :return: logger instance
    """
    logger_r = logging.getLogger('my_logger')
    logger_r.setLevel(logging.DEBUG)

    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(logging.DEBUG)
    file_handler = logging.FileHandler('log_file.txt')

    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    stream_handler.setFormatter(formatter)
    file_handler.setFormatter(formatter)
    logger_r.addHandler(stream_handler)
    logger_r.addHandler(file_handler)

    return logger_r


logger = define_logger()
