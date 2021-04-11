"""
A service to store host information in the db
"""
import datetime
import sqlite3

from core import generate_log as logger
from core import input_command


@logger.wrap(logger.enter, logger.exit)
def run():
    """
    The method to gather host information and store it in the db
    """
    dateTime = datetime.datetime.now()
    # "%Y-%m-%d %H:%M:%S:%f" is default formatting with everything
    dateTime = dateTime.strftime("%m-%d-%y %H:%M:%S")

    numCoresCommand = "sysctl -n hw.logicalcpu"
    numCores = int(input_command.run(numCoresCommand))

    osVersionCommand = "sw_vers | grep ProductVersion | awk '{s=$2} END {print s}'"
    osVersion = input_command.run(osVersionCommand)

    totalDiskCommand = "df | grep '/$' | awk '{s=$2} END {print s}'"
    totalDiskBlocks = int(input_command.run(totalDiskCommand))
    totalDiskGB = totalDiskBlocks * 512 / 1000 ** 3

    totalRamCommand = "sysctl hw.memsize | awk '{s=$2} END {print s}'"
    totalRamBytes = int(input_command.run(totalRamCommand))
    totalRamGB = totalRamBytes / 1024 ** 3

    host = [dateTime, numCores, osVersion, totalDiskGB, totalRamGB]
    con = sqlite3.connect("db/prism.db")
    cur = con.cursor()
    cur.execute("INSERT INTO host VALUES (NULL,?,?,?,?,?)", host)
    con.commit()
    cur.close()
    con.close()
