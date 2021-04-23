"""
A service to store host information in the db
"""
import sqlite3

from core import conversion
from core import generate_log as logger
from core import input_command, time


@logger.wrap(logger.enter, logger.exit)
def run(db_file):
    """
    The method to gather host information and store it in the db
    - db_file: (string) The path to the database file
    """
    dateTime = time.get_current_time()

    logger.logger.info("Executing and storing host data")

    numCoresCommand = "sysctl -n hw.logicalcpu"
    numCores = int(input_command.run(numCoresCommand))

    osVersionCommand = "sw_vers | grep ProductVersion | awk '{s=$2} END {print s}'"
    osVersion = input_command.run(osVersionCommand)

    totalDiskCommand = "df | grep '/$' | awk '{s=$2} END {print s}'"
    totalDiskBlocks = int(input_command.run(totalDiskCommand))
    totalDiskGB = conversion.blocks_to_gb(totalDiskBlocks)

    totalRamCommand = "sysctl hw.memsize | awk '{s=$2} END {print s}'"
    totalRamBytes = int(input_command.run(totalRamCommand))
    totalRamGB = conversion.bytes_to_gb(totalRamBytes)

    host = [dateTime, numCores, osVersion, totalDiskGB, totalRamGB]
    con = sqlite3.connect(db_file)
    cur = con.cursor()
    cur.execute("INSERT INTO host VALUES (NULL,?,?,?,?,?)", host)
    con.commit()
    cur.close()
    con.close()
