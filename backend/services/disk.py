"""
A service to store disk information in the db
"""
import sqlite3

from core import conversion, db_query
from core import generate_log as logger
from core import input_command, time


@logger.wrap(logger.enter, logger.exit)
def run(count, db_file):
    """
    The method to gather disk information and store it in the db
    - count: (int) The iteration of the current run
    - db_file: (string) The path to the database file
    """
    logger.logger.info("Executing and storing disk data")

    hostId = db_query.max_host_id()

    dateTime = time.get_current_time()

    usedDiskCommand = "df | tail +2 | awk '{s+=$3} END {print s}'"
    usedDiskBlocks = int(input_command.run(usedDiskCommand))
    usedDiskGB = conversion.blocks_to_gb(usedDiskBlocks)

    disk = [hostId, count, dateTime, usedDiskGB]
    con = sqlite3.connect(db_file)
    cur = con.cursor()
    cur.execute("INSERT INTO disk VALUES (NULL,?,?,?,?)", disk)
    con.commit()
    cur.close()
    con.close()
    logger.logger.info("Stored disk: {}".format(disk))
