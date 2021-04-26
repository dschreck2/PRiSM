"""
A file to get time information
"""
import datetime

from core import generate_log as logger


@logger.wrap(logger.enter, logger.exit)
def get_current_time():
    """
    Get and format the current date and time
    """
    dateTime = datetime.datetime.now()
    # "%Y-%m-%d %H:%M:%S:%f" is default formatting with everything
    dateTime = dateTime.strftime("%m-%d-%y %H:%M:%S")

    logger.logger.debug("Getting current time: {}".format(dateTime))

    return dateTime
