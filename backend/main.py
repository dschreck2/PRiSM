"""
The main file to store PRiSM data in the database
"""

import os
import pathlib

from core import generate_log as logger
from services import cpu, disk, host, process, ram


@logger.wrap(logger.enter, logger.exit)
def main():
    path = pathlib.Path(__file__).parent.absolute()
    run_file = "{}/../run.txt".format(path)

    try:
        f = open(run_file, "x")
        host.run()
        while os.path.exists(run_file):
            cpu.run()
            disk.run()
            process.run()
            ram.run()
        f.close()

    except FileExistsError as e:
        logger.logger.info(e)
        logger.logger.info("Already running, don't run again")


if __name__ == "__main__":
    main()
