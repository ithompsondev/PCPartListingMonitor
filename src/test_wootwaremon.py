import unittest
import unittest.mock as mock
from io import TextIOBase
from listinggen import BaseListingGenerator
from wootwaremon import WootwareListingGenerator
from listing import Listing

"""
    A dummy class used to replicate the Response class from the requests module
"""


class ResponseMock:
    def __init__(self, html: TextIOBase):
        self.text = self.__condense(html.readlines(), by="")

    # Condense a list of strings into a single string separated by a given delimiter
    @staticmethod
    def __condense(strings: list, by: str) -> str:
        return by.join(strings)


"""
    We choose to only test the public methods by creating test cases where we are able to control
    the circumstance for how the private methods within these public method invocations are called.
"""


# Accessing private members of a class -> _MyClassName__private_member
class TestWootwaremon(unittest.TestCase):
    def test_parse_for_empty_listings_txt(self):
        empty_file = open("test/resource/empty_file.txt", "r")

        """
            Here we mock the method WootwareListingGen inherits from the superclass for getting product
            listings from a file. We essentially hijack the method call and tell it what to return, which is an
            opened empty file for reading located in the test/resource directory instead of reading from system critical
            text file: listings.txt
        """
        with mock.patch.object(BaseListingGenerator, "_BaseListingGenerator__get_product_listings", return_value=empty_file) as gpl_mock:
            woot_listing = WootwareListingGenerator()

            actual_parsed_prod_list = woot_listing.parse_listings()
            expected_parsed_prod_list = []
            self.assertListEqual(actual_parsed_prod_list, expected_parsed_prod_list)
            empty_file.close()

    def test_parse_for_valid_non_empty_listings_txt(self):
        # Open file containing a valid listings.txt file (Link to the product)
        valid_listings_test = open("test/resource/valid_listings_test.txt", "r")
        # Open file containing the raw HTML of the above listing, simulating (_scrape_listing(listing)).text
        html: TextIOBase = open("test/resource/woot_test_product_listing.html", "r")
        woot_test_product_listing = ResponseMock(html)

        # mock the methods to scrape a listing and open a listing.txt file containing the links to product lisings
        # Remember mocking the methods allow us to hijack their control when they are invoked
        with mock.patch.object(BaseListingGenerator, "_scrape_listing", return_value=woot_test_product_listing) as html_mock:
            with mock.patch.object(BaseListingGenerator, "_BaseListingGenerator__get_product_listings", return_value=valid_listings_test) as gpl_mock:
                woot_listing = WootwareListingGenerator()

                actual_parsed_prod_list = woot_listing.parse_listings()
                expected_parsed_prod_list = [
                    Listing()
                    .title("Corsair\xa0CMH32GX4M2E3200C16 Vengeance RGB Pro SL 32GB (2x16GB) DDR4-3200MHz CL16 1.35V Black Desktop Memory")
                    .link("https://www.wootware.co.za/corsair-cmh32gx4m2e3200c16-vengeance-rgb-pro-sl-32gb-2x16gb-ddr4-3200mhz-cl16-1-35v-black-desktop-memory.html")
                ]

                self.assertEqual(actual_parsed_prod_list[0], expected_parsed_prod_list[0])


unittest.main()
