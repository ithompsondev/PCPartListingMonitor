import enum
import os
import pickle
from listing import Listing, ListingChange
from respathing import *
from constants import Change

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
    def monitor_changes(self, prev_product_listings: list, curr_product_listings: list):
        for product in curr_product_listings:
            curr_new_price = product.get_price()

            change = None
            if product in prev_product_listings:
                prev_listed_price = self.__get_previously_listed_price(product, prev_product_listings)
                change = ListingChange(product, self.__compare_price_changes(curr_new_price, prev_listed_price))
            else:
                if curr_new_price == 0.0:
                    change = ListingChange(product, Change.OUT_STOCK)  # useful when monitor is initially run
                else:
                    change = ListingChange(product, Change.NEW)
            self.__changes.append(change)

        # Loop through previously saved product listings and compare them against the new product listings
        # If a product in the previously saved listing dne in the new listings then this means that the product
        # will no longer be monitored
        for pre_product in prev_product_listings:
            # The product is no longer being monitored
            still_monitored = pre_product in curr_product_listings
            if not still_monitored:
                self.__changes.append(ListingChange(pre_product, Change.REMOVED))
        if self.__notifier is not None:
            self.__notifier.make_notification(self.__changes)

    @staticmethod
    def __compare_price_changes(new_price: float, old_price: float) -> 'Change':
        if new_price > old_price:
            if old_price == 0.0:
                return Change.IN_STOCK  # useful when monitoring is already in progress
            return Change.NEGATIVE
        elif new_price < old_price:
            if new_price == 0.0:
                return Change.OUT_STOCK
            return Change.POSITIVE
        else:
            return Change.SAME

    @staticmethod
    def __get_previously_listed_price(product: Listing, prev_product_listings: list) -> float:
        i = prev_product_listings.index(product)
        return prev_product_listings[i].get_price()

    def get_changes(self):
        return self.__changes

    def get_notifier(self):
        return self.__notifier


