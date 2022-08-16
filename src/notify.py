from abc import ABC, abstractmethod
from datetime import datetime
import os
from monitor import Change

divider = "="*80

"""
    A notifier should keep track of whether it is the first time it is running.
    Useful for logging a welcome message.
"""

# TODO: os.path.join(sys.path[0], "product_listings.lt") where sys.path[0] is the absolute root path of the script
# TODO: os.path.join(sys.path[0], "listings_log.txt")
class Notifier(ABC):
    def __init__(self, title: str):
        self._title = title
        self._first_run = not os.path.exists("product_listings.lt")

    @abstractmethod
    def make_notification(self, changes: list):
        pass


class LogDumpNotifier(Notifier):
    def __int__(self, title):
        super().__init__(title)

    def make_notification(self, changes: list):
        log = open("listing_log.txt", "a")
        any_changes = False
        if self._first_run:
            log.write(f"[{datetime.now()}] Starting new product listing monitor as {self._title}.\n\n")

        for change in changes:
            curr_change = change.get_change()
            listing = str(change.get_listing())
            if self.__has_changed(curr_change):
                if not any_changes:
                    # We use this flag to know when to write out section divider
                    any_changes = True
                if curr_change == Change.POSITIVE:
                    log.write("Good News! The price for this product has decreased.\n")
                elif curr_change == Change.NEGATIVE:
                    log.write("Bad News! The price for this product has increased.\n")
                elif curr_change == Change.REMOVED:
                    log.write("The following product is no longer being monitored, \n")
                else:
                    log.write("New Listing! Monitoring for this product has now begun.\n")
                log.write(f"{listing}\n")
        if any_changes:
            log.write(divider + "\n\n")
        else:
            log.write(f"[{datetime.now()}] No changes monitored for any listing.\n\n")
            log.write(divider + "\n\n")
        log.close()

    @staticmethod
    def __has_changed(change):
        return change == Change.POSITIVE or \
               change == Change.NEGATIVE or \
               change == Change.NEW or \
               change == Change.REMOVED
