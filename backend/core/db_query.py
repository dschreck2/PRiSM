"""
A file to query the DB for information needed by the backend
"""
import pathlib
import sqlite3

from core import generate_log as logger


@logger.wrap(logger.enter, logger.exit)
def max_host_id():
    """
    Query the max host ID
    """
    path = pathlib.Path(__file__).parent.absolute()
    con = sqlite3.connect("{}/../../db/prism.db".format(path))
    cur = con.cursor()

    cur.execute("SELECT MAX(id) FROM host;")
    hostId = cur.fetchone()[0]
    logger.logger.debug("Query the current host ID: {}".format(hostId))

    con.commit()
    cur.close()
    con.close()

    return hostId
