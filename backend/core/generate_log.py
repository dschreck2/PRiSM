"""Logging file to create a global Logger instance"""

import logging
import pathlib
import sys
from logging import handlers


def create_file_handler(log_name):
    """
    creates file logging output
    - log_name: (string) the config file
    """
    file_handler = handlers.TimedRotatingFileHandler(
        log_name, when="midnight", interval=1
    )
    file_handler.suffix = "%Y%m%d"
    file_handler.setFormatter(formatter)
    return file_handler


def traceback_hook(type, value, traceback):
    """
    Prints stack trace to log if an uncaught error is encountered
    """
    logger.error("Uncaught Error:", exc_info=(type, value, traceback))


def wrap(pre, post):
    """ Wrapper """

    def decorate(func):
        """ Decorator """

        def call(*args, **kwargs):
            """ Actual wrapping """
            pre(func)
            result = func(*args, **kwargs)
            post(func)
            return result

        return call

    return decorate


def enter(func):
    """ Pre function logging """
    logger.debug("{}.{} ->".format(func.__code__.co_filename, func.__name__))


def exit(func):
    """ Post function logging """
    logger.debug("{}.{} <-".format(func.__code__.co_filename, func.__name__))


logger = logging.getLogger("PRiSM")
formatter = logging.Formatter(
    "%(asctime)s - %(levelname)s - %(filename)s - %(funcName)s - %(message)s"
)

path = pathlib.Path(__file__).parent.absolute()

logger.addHandler(create_file_handler("{}/../logs/prismlog.txt".format(path)))
logger.setLevel(logging.INFO)

logger.debug("Log file located: {}".format("{}/../logs/prismlog.txt".format(path)))
sys.excepthook = traceback_hook
logger.debug("Logger Initialized")
