"""
A service to store process information in the db
"""
import sqlite3

from core import db_query
from core import generate_log as logger
from core import input_command, time


@logger.wrap(logger.enter, logger.exit)
def run():
    """
    The method to gather process information and store it in the db
    """
    hostId = db_query.max_host_id()

    dateTime = time.get_current_time()

    processInfoCommand = "ps -arcwwwxo 'command pid ppid %mem %cpu user etime time'"
    processInfo = input_command.run(processInfoCommand)
    processInfo = processInfo.split("\n")
    processInfo.pop(0)  # Remove header column
    processInfo.pop(-1)  # Remove empty list at end
    for line in processInfo:
        line = line.split()
        pid = line[-7]
        ppid = line[-6]
        memoryUsage = line[-5]
        cpuUsage = line[-4]
        userName = line[-3]
        wallTime = line[-2]
        cpuTime = line[-1]
        for index, element in enumerate(line):
            if element == pid:
                processName = " ".join(line[:index])
                break
        threadsCommand = "ps -M {} | wc -l".format(pid)
        threads = int(input_command.run(threadsCommand))

        process = [
            hostId,
            dateTime,
            processName,
            pid,
            ppid,
            memoryUsage,
            cpuUsage,
            userName,
            threads,
            wallTime,
            cpuTime,
        ]
        con = sqlite3.connect("db/prism.db")
        cur = con.cursor()
        cur.execute("INSERT INTO process VALUES (NULL,?,?,?,?,?,?,?,?,?,?,?)", process)
        con.commit()
        cur.close()
        con.close()
