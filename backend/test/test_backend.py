"""
This file is for unit testing of the backend
"""
# Imports used to test
import os
import sys

# Set testing path to find backend files
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))


# Imports to test
from core import conversion


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
