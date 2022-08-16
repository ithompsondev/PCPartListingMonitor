import enum
import os
import pickle
import listing
from respathing import *

# TODO: os.path.join(sys.path[0], "product_listings.lt") where sys.path[0] is the absolute root path of the script
SAVE_FILE = path_to_saved_listings()


# Make a base monitor, this monitor is for wootware
class Monitor:
    def __init__(self, notifier):
        self.__changes = []
        self.__notifier = notifier

    """
        Serialize a list of Listing objects to the file
        named product_listings.lt
    """

    @staticmethod
    def save_product_listings(product_listings: list):
        save_file = open(SAVE_FILE, "wb")
        pickle.dump(product_listings, save_file)
        save_file.close()

    """
        If the file: product_listings.lt exists then load its 
        contents into a list. If it does not contain previously
        saved product listings return an empty list, otherwise return
        the loaded product listings
    """

    @staticmethod
    def load_product_listings() -> list:
        if os.path.exists(SAVE_FILE):
            save_file = open(SAVE_FILE, "rb")
            loaded_listings = pickle.load(save_file)
            save_file.close()

            if loaded_listings is None:
                loaded_listings = []
            else:
                print("Loaded previous product listings from: " + SAVE_FILE)
            return loaded_listings
        else:
            print("No previous product listings have been saved.")
            return []

    """
        Monitor the changes between the old product listings, loaded from 
        a saved product listings file, with the newly created product listings, 
        from scraping/parsing from a ListingGenerator. All changes, even no change,
        is saved to a list of ListingChanges objects. The list of ListingChanges
        will be passed to the notifier to notify subscribed users of changes.
        
        We also need to ensure that we compare the same products to be able to monitor
        a change in their prices. Since we implemented __eq__ for Listing we can check if
        a listing exists in a list of listings and compare the same products accordingly.
    """

    # TODO: Case where listing saved file exists but a log does not!
    def monitor_changes(self, pre_product_listings: list, product_listings: list):
        for product in product_listings:
            curr_price = product.get_price()
            change = None
            if product in pre_product_listings:
                i = pre_product_listings.index(product)
                old_price = pre_product_listings[i].get_price()

                if curr_price > old_price:
                    change = listing.ListingChange(product, Change.NEGATIVE)
                elif curr_price < old_price:
                    change = listing.ListingChange(product, Change.POSITIVE)
                else:
                    change = listing.ListingChange(product, Change.SAME)
            else:
                change = listing.ListingChange(product, Change.NEW)
            self.__changes.append(change)

        for pre_product in pre_product_listings:
            # The product is no longer being monitored
            still_monitored = pre_product in product_listings
            if not still_monitored:
                self.__changes.append(listing.ListingChange(pre_product, Change.REMOVED))
        if self.__notifier is not None:
            self.__notifier.make_notification(self.__changes)

    def get_changes(self):
        return self.__changes

    def get_notifier(self):
        return self.__notifier


class Change(enum.Enum):
    NEGATIVE = 0,
    POSITIVE = 1,
    SAME = 2,
    NEW = 3,
    REMOVED = 4

