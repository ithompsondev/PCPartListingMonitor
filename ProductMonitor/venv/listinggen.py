from io import TextIOBase
from typing import Union
import requests
from abc import ABC, abstractmethod

"""
    Read product listings from a text file named listings.txt
    this rigidness in design is intentional. TODO: need more
    description
"""


class BaseListingGenerator(ABC):
    def __init__(self):
        self._listings: TextIOBase = self.__get_product_listings()

    @staticmethod
    def __get_product_listings() -> TextIOBase:
        try:
            return open("listings.txt", "r")
        except FileNotFoundError:
            print("The product listings file: listings.txt, could not be found.")
            print("Ensure that the listings.txt file is in the same directory as this script.")

    """
        Scrape a listing from a given URL
    """

    @staticmethod
    def _scrape_listing(listing: str) -> Union[requests.Response, None]:
        response = None
        try:
            listing = listing.rstrip("\n")
            response = requests.get(listing)
            status = response.status_code

            print("The listing for: " + listing + ", returned with status code: " + str(status))
            if status != 200:
                raise BadResponseException(
                    "The listing for: " + listing + ", returned with a bad response [status: " + str(status) + "]"
                )
        except requests.ConnectionError:
            print("There was a problem connecting to: " + listing)
        except requests.Timeout:
            print("The listing at: " + listing + ", took too long to respond")
            system.exit(1)
        except requests.exceptions.RequestException as req_ex:
            print("A problem was encountered when scraping the listing for: " + listing)
            print(req_ex)
        finally:
            return response

    """
        Concrete classes must provide an implementation for parsing the scraped html for
        a listing. This is dependant on the website a listing originates from.
    """

    @abstractmethod
    def parse_listings(self):
        pass


class BadResponseException(Exception):
    def __init__(self, message: str):
        super().__init__(message)


def main():
    product_listings = get_product_listings()


if __name__ == "__main__":
    main()

