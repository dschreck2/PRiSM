"""
This file is for unit testing of the backend
"""
# Imports used to test
import os
import pathlib
import sys

# Set testing path to find backend files
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))


import main
from core import conversion, generate_log
from main import db_file, run_file

path = pathlib.Path(__file__).parent.absolute()
log_file = "{}/../logs/prismlog.txt".format(path)


def test_generate_log_traceback_hook():
    """
    Test the logger error handling exception hook
    """
    try:
        1 / 0
    except ZeroDivisionError:
        generate_log.traceback_hook(*sys.exc_info())
        f = open(log_file, "r")
        log = f.read().splitlines()
        f.close()
        assert log[-1] == "ZeroDivisionError: division by zero"


def test_run_main():
    """
    Test the main file with a run_file already existing
    """
    # Create run file
    if not os.path.exists(run_file):
        f = open(run_file, "x")
        f.close()

    assert main.main(0) == 0


def test_fresh_main():
    """
    Test the main file with no run_file or db_file
    """
    # Delete run file
    if os.path.exists(run_file):
        os.remove(run_file)

    # Delete db file
    if os.path.exists(db_file):
        os.remove(db_file)

    assert main.main(2) == 0


def test_conversion_blocks_to_gb():
    """
    Tests core.conversion.blocks_to_gb()
    """
    blocks = 976562500
    assert conversion.blocks_to_gb(blocks) == 500


def test_conversion_bytes_to_gb():
    """
    Tests core.conversion.bytes_to_gb()
    """
    bytes = 17179869184
    assert conversion.bytes_to_gb(bytes) == 16


def test_conversion_pages_to_gb():
    """
    Tests core.conversion.pages_to_gb()
    """
    pages = 524288
    assert conversion.pages_to_gb(pages) == 2
