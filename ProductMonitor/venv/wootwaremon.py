import re
from listinggen import BaseListingGenerator
from bs4 import BeautifulSoup as BSoup
from datetime import datetime
from listing import Listing
from typing import Union


class WootwareListingGenerator(BaseListingGenerator):
    def __init__(self, prev_product_listings=[]):
        super().__init__()
        self.__product_listings = prev_product_listings

    """
        Simply check whether the URL given by a listing contains
        the substring provided
    """

    @staticmethod
    def __validate_url(listing: str):
        if "wootware.co.za" not in listing:
            return False

    """
        For each listing, first validate the URL. If an invalid URL is
        encountered, just skip parsing it. Then scrape each URL for the HTML
        content and begin parsing
        
        First extract the product name, then extract the product image url. Finally,
        the products base/old price and current/special price is extracted.
        
        Once all required information is parsed and extracted form the HTML from the 
        scraped listing, a new Listing object is created and appended to a list. If
        no previous listings have been loaded we set this ListingGenerators product listings
        list to the newly generated product listings list then return the newly generated list. 
        If a previous listing has been loaded we only return the newly generated listing.
        
        Case 1: No product listings have been saved before, self.__product_listings = []
                so that when this method returns new product listings we know that they are new
                since there is nothing to compare them to
        Case 2: Product listings have been saved before, self.__product_listings = loaded listings (from monitor)
                so that when this method returns new product listings we can now compare it to the old
                loaded product listings
    """

    def parse_listings(self) -> Union[list, None]:
        latest_product_listings = []
        for listing in self._listings:
            if self.__validate_url(listing) is False:
                continue

            response = (self._scrape_listing(listing)).text
            if response is not None:
                soup_data = BSoup(response, "html.parser")
                product_name = list(
                    map(
                        lambda html: html.get_text(),
                        soup_data.findAll("h1", {"itemprop": "name"})
                    )
                )[0]
                product_image = list(
                    map(
                        lambda image: image["data-src"],
                        soup_data.findAll("img", {"width": 512, "height": 512})
                    )
                )[0]
                product_old_pricing, product_pricing = self.__get_pricing(soup_data)
                product_check_date = datetime.now()

                latest_product_listings.append(
                    Listing()
                    .title(product_name)
                    .img(product_image)
                    .pre_price(product_old_pricing)
                    .sp_price(product_pricing)
                    .date(product_check_date)
                    .link(listing)
                )
            else:
                print("No valid response obtained for listing: " + listing)

        # The monitor should handle checking for changes and pickling etc
        return latest_product_listings

    def get_product_listings(self) -> list:
        return self.__product_listings

    def show_listings(self):
        for listing in self.__product_listings:
            print(listing)
            print()

    """
        From the BSoup html retrieved after scraping the listing from the given URL
        the DIV used to contain the pricing information is retrieved. Since the prices
        are contained withing span elements (specific to wootware), they can be obtained from
        the DIV container. Lastly , for each element in the list of SPAN elements, the relevant
        prices are obtained by checking if the id attribute matches a given string.
    """

    @staticmethod
    def __get_pricing(soup_data: BSoup):
        pricing_container = soup_data.find("div", {"class", "add-to-cart-wrapper"})
        prices = pricing_container.findAll("span")

        old_price_partial = "old-price"
        curr_price_partial = "product-price"
        old_price, curr_price = None, None
        for price in prices:
            price_id = price.get("id")
            if price_id is not None:
                if old_price_partial in price_id:
                    old_price = price.get_text()
                if curr_price_partial in price_id:
                    curr_price = price.get_text()

        old_price = 0.0 if old_price is None else float(old_price.replace("R", "").replace(",", ""))
        curr_price = 0.0 if curr_price is None else float(curr_price.replace("R", "").replace(",", ""))
        return old_price, curr_price

