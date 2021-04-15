"""
The main file to store PRiSM data in the database
"""

from core import generate_log as logger
#from core import read_config
from services import cpu, disk, host, process, ram


@logger.wrap(logger.enter, logger.exit)
def main():
'''
    if read_config.config["is_running"]:
        host.run()
        cpu.run()
        disk.run()
        process.run()
        ram.run()
'''

if __name__ == "__main__":
    main()
