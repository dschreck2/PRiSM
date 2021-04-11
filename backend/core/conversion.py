"""
A file to perform mathematical unit conversions
"""

from core import generate_log as logger


@logger.wrap(logger.enter, logger.exit)
def blocks_to_gb(blocks):
    """
    Convert 512 byte blocks to gigabytes
    """
    return blocks * 512 / 1000 ** 3


@logger.wrap(logger.enter, logger.exit)
def bytes_to_gb(bytes):
    """
    Convert bytes to gigabytes
    """
    return bytes / 1024 ** 3


@logger.wrap(logger.enter, logger.exit)
def pages_to_gb(pages):
    """
    Convert bytes to gigabytes
    """
    return pages * 4096 / 1024 ** 3
