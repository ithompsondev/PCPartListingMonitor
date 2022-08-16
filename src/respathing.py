import os
import sys

"""
    Provide a platform independent method for locating and accessing
    files required for the script to run correctly.
"""

# TODO: Test on windows
SCRIPT_PATH = sys.path[0]
LISTINGS_WIN = "listings.txt.txt"
LISTINGS_LOG_WIN = "listings_log.txt.txt"
LISTINGS_UNIX = "listings.txt"
LISTINGS_LOG_UNIX = "listings_log.txt"
SAVED_LISTINGS = "product_listings.lt"


def path_to_listings_win():
    return os.path.join(SCRIPT_PATH, LISTINGS_WIN)


def path_to_listings_unix():
    return os.path.join(SCRIPT_PATH, LISTINGS_UNIX)


def path_to_listings_log_win():
    return os.path.join(SCRIPT_PATH, LISTINGS_LOG_WIN)


def path_to_listings_log_unix():
    return os.path.join(SCRIPT_PATH, LISTINGS_LOG_UNIX)


def path_to_saved_listings():
    return os.path.join(SCRIPT_PATH, SAVED_LISTINGS)


def is_windows():
    return sys.platform == "win32"
