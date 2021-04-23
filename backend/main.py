"""
The main file to store PRiSM data in the database
"""

import datetime
import os
import pathlib
import time

from core import generate_log as logger
from services import cpu, create_db, disk, host, process, prune, ram


@logger.wrap(logger.enter, logger.exit)
def main():
    path = pathlib.Path(__file__).parent.absolute()
    run_file = "{}/../run.txt".format(path)
    db_file = "{}/../db/prism.db".format(path)
    schema_file = "{}/../db/schema.txt".format(path)

    if not os.path.exists(db_file):
        logger.logger.info("DB File does not exist")
        create_db.run(db_file, schema_file)
    else:
        logger.logger.info("DB File exists")

    try:
        f = open(run_file, "x")
        f.close()
        host.run(db_file)
        count = 0
        currentTime = datetime.datetime.now()
        # Run first loop immediately
        executeTime = currentTime
        while os.path.exists(run_file):
            currentTime = datetime.datetime.now()
            if currentTime >= executeTime:
                # Executing in 15 second intervals
                executeTime = currentTime + datetime.timedelta(seconds=15)
                count += 1
                cpu.run(count, db_file)
                disk.run(count, db_file)
                process.run(count, db_file)
                ram.run(count, db_file)
                prune.run(count, db_file)
            else:
                time.sleep(0.001)

    except FileExistsError as e:
        logger.logger.info(e)
        logger.logger.info("Already running, don't run again")


if __name__ == "__main__":
    main()
