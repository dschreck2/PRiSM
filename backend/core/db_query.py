"""
A file to query the DB for information needed by the backend
"""
import sqlite3

from core import generate_log as logger


@logger.wrap(logger.enter, logger.exit)
def max_host_id(db_file):
    """
    Query the max host ID
    """
    con = sqlite3.connect(db_file)
    cur = con.cursor()

    cur.execute("SELECT MAX(id) FROM host;")
    hostId = cur.fetchone()[0]
    logger.logger.debug("Query the current host ID: {}".format(hostId))

    con.commit()
    cur.close()
    con.close()

    return hostId
