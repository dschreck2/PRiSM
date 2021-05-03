"""
A service to prune old information from the db
"""
import sqlite3

from core import db_query
from core import generate_log as logger


@logger.wrap(logger.enter, logger.exit)
def run(count, db_file):
    """
    The method to prune old information from the DB

    Each count is 15 seconds
    We need to keep last full minute, which is 4 counts
    We also need to keep last 10 minutes of 1 minutes counts
    1 minute counts are 1, 5, 9, 13, 17, 21, 25, 29, 33, 37, 41, 45, etc.
    We permanently keep 10 minute counts
    10 minutes counts are 1, 41, 81, 121, etc.

    - count: (int) The iteration of the current run
    - db_file: (string) The path to the database file
    """
    hostId = db_query.max_host_id()

    tables = ["cpu", "disk", "process", "ram"]

    con = sqlite3.connect(db_file)
    cur = con.cursor()

    # At 6 prune 2, at 7 prune 3, at 8 prune 4, skip 9, at 10 prune 6, etc.
    if count >= 6 and count % 4 != 1:
        logger.logger.info("Count is {}, pruning {}".format(count, count - 4))
        for table in tables:
            prune = [hostId, count - 4]
            cur.execute(
                "DELETE FROM {} WHERE hostId=? AND count=?".format(table), prune
            )

    # At 45 prune 5, ... at 77 prune 37, skip 81, at 85 prune 45
    if count >= 45 and count % 4 == 1 and count % 41 != 1:
        logger.logger.info("Count is {}, pruning {}".format(count, count - 40))
        for table in tables:
            prune = [hostId, count - 40]
            cur.execute(
                "DELETE FROM {} WHERE hostId=? AND count=?".format(table), prune
            )

    con.commit()
    cur.close()
    con.close()
