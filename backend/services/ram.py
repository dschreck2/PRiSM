"""
A service to store ram information in the db
"""
import sqlite3

from core import conversion, db_query
from core import generate_log as logger
from core import input_command, time


@logger.wrap(logger.enter, logger.exit)
def run(count, db_file):
    """
    The method to gather ram information and store it in the db
    - count: (int) The iteration of the current run
    - db_file: (string) The path to the database file
    """
    logger.logger.info("Executing and storing RAM data")

    hostId = db_query.max_host_id()

    dateTime = time.get_current_time()

    internalPageCountCommand = (
        "sysctl vm.page_pageable_internal_count | awk '{s=$2} END {print s}'"
    )
    internalPageCount = int(input_command.run(internalPageCountCommand))

    purgeablePagesCommand = (
        "vm_stat | grep 'Pages purgeable:' | awk '{s+=$3} END {print s}'"
    )
    purgeablePages = int(input_command.run(purgeablePagesCommand))

    appMemory = internalPageCount - purgeablePages

    wiredMemoryCommand = (
        "vm_stat | grep 'Pages wired down:' | awk '{s+=$4} END {print s}'"
    )
    wiredMemory = int(input_command.run(wiredMemoryCommand))

    compressedMemoryCommand = (
        "vm_stat | grep 'Pages occupied by compressor:' | awk '{s+=$5} END {print s}'"
    )
    compressedMemory = int(input_command.run(compressedMemoryCommand))

    usedRamPages = appMemory + wiredMemory + compressedMemory
    usedRamGB = conversion.pages_to_gb(usedRamPages)

    ram = [hostId, count, dateTime, usedRamGB]
    con = sqlite3.connect(db_file)
    cur = con.cursor()
    cur.execute("INSERT INTO ram VALUES (NULL,?,?,?,?)", ram)
    con.commit()
    cur.close()
    con.close()
    logger.logger.info("Stored ram: {}".format(ram))
