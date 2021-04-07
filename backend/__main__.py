"""
The main file to store PRiSM data in the database
"""

from core import generate_log as logger
from core import read_config

@logger.wrap(logger.enter, logger.exit)
def main():
    if read_config.config["is_running"]:
        print("Hello, World!")

if __name__ == '__main__':
    main()
