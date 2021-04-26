"""
A service to store cpu information in the db
"""
import sqlite3

from core import db_query
from core import generate_log as logger
from core import input_command, time


@logger.wrap(logger.enter, logger.exit)
def run(count, db_file):
    """
    The method to gather cpu information and store it in the db
    - count: (int) The iteration of the current run
    - db_file: (string) The path to the database file
    """
    logger.logger.info("Executing and storing CPU data")

    hostId = db_query.max_host_id()

    dateTime = time.get_current_time()

    usedCPUCommand = "ps -A -o %cpu | awk '{s+=$1} END {print s}'"
    usedCPU = float(input_command.run(usedCPUCommand))

    cpu = [hostId, count, dateTime, usedCPU]
    logger.logger.info("Stored cpu: {}".format(cpu))
    con = sqlite3.connect(db_file)
    cur = con.cursor()
    cur.execute("INSERT INTO cpu VALUES (NULL,?,?,?,?)", cpu)
    con.commit()
    cur.close()
    con.close()
