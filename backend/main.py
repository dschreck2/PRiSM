"""
The main file to store PRiSM data in the database
"""

import datetime
import os
import pathlib
import time

from core import db_query
from core import generate_log as logger
from services import cpu, create_db, disk, host, process, prune, ram

path = pathlib.Path(__file__).parent.absolute()
run_file = "{}/../run.txt".format(path)
db_file = "{}/../db/prism.db".format(path)
schema_file = "{}/../db/schema.txt".format(path)


@logger.wrap(logger.enter, logger.exit)
def main(test_loops=-1):

    if not os.path.exists(db_file):
        logger.logger.info("DB File does not exist")
        create_db.run(db_file, schema_file)
    else:
        logger.logger.info("DB File exists")

    try:
        f = open(run_file, "x")
        f.close()

        host.run(db_file)
        hostId = db_query.max_host_id(db_file)

        count = 0
        currentTime = datetime.datetime.now()
        # Run first loop immediately
        executeTime = currentTime
        while os.path.exists(run_file) and (test_loops >= 1 or test_loops <= -1):
            currentTime = datetime.datetime.now()
            if currentTime >= executeTime:
                # Executing in 15 second intervals
                executeTime = currentTime + datetime.timedelta(seconds=15)
                count += 1
                cpu.run(count, hostId, db_file)
                disk.run(count, hostId, db_file)
                ram.run(count, hostId, db_file)
                process.run(count, hostId, db_file)
                prune.run(count, hostId, db_file)
                test_loops -= 1
            else:
                time.sleep(0.001)
        if os.path.exists(run_file):
            logger.logger.info("Run file exists, deleting")
            os.remove(run_file)

        logger.logger.info("Run file no longer exists, ending")

    except FileExistsError as e:
        logger.logger.info(e)
        logger.logger.info("Run file exists, don't run again")
    return 0


if __name__ == "__main__":
    main()
