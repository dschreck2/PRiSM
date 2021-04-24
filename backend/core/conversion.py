"""
A file to perform mathematical unit conversions
"""

from core import generate_log as logger


@logger.wrap(logger.enter, logger.exit)
def blocks_to_gb(blocks):
    """
    Convert 512 byte blocks to gigabytes
    """
    gb = blocks * 512 / 1000 ** 3
    logger.logger.debug("Blocks: {}, Gigabytes: {}".format(blocks, gb))
    return gb


@logger.wrap(logger.enter, logger.exit)
def bytes_to_gb(bytes):
    """
    Convert bytes to gigabytes
    """
    gb = bytes / 1024 ** 3
    logger.logger.debug("Bytes: {}, Gigabytes: {}".format(bytes, gb))
    return gb


@logger.wrap(logger.enter, logger.exit)
def pages_to_gb(pages):
    """
    Convert pages to gigabytes
    """
    gb = pages * 4096 / 1024 ** 3
    logger.logger.debug("Pages: {}, Gigabytes: {}".format(pages, gb))
    return gb
