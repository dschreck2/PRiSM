"""
A service to create the db, if the file does not exist
"""
import sqlite3

from core import generate_log as logger


@logger.wrap(logger.enter, logger.exit)
def run(db_file, schema_file):
    try:
        logger.logger.info("Creating database")
        f = open(db_file, "x")
        f.close()
    except FileExistsError as e:
        logger.logger.info(e)
        logger.logger.info("DB file exists, this shouldn't be possible")

    f = open(schema_file, "r")
    schema = f.read()
    f.close()

    con = sqlite3.connect(db_file)
    cur = con.cursor()
    cur.executescript(schema)
    con.commit()
    cur.close()
    con.close()
