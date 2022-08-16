from typing import Union
from datetime import datetime
from monitor import Change

# convert to dataclass?


class Listing:
    def __init__(self):
        self.__name: Union[str, None] = None
        self.__url: Union[str, None] = None
        self.__img_url: Union[str, None] = None
        self.__old_price: Union[float, None] = 0.0
        self.__price: Union[float, None] = 0.0
        self.__date_of_last_check: Union[datetime, None] = None

    def get_title(self):
        return self.__name

    def get_url(self):
        return self.__url

    def get_img_url(self):
        return self.__img_url

    def get_old_price(self):
        return self.__old_price

    def get_price(self):
        return self.__price

    def get_date(self):
        return self.__date_of_last_check

    def title(self, name: str):
        self.__name = name
        return self

    def link(self, url: str):
        self.__url = url
        return self

    def img(self, img_url: str):
        self.__img_url = img_url
        return self

    def pre_price(self, old_price: float):
        self.__old_price = old_price
        return self

    def sp_price(self, price: float):
        self.__price = price
        return self

    def date(self, date: datetime):
        self.__date_of_last_check = date
        return self

    def __eq__(self, other):
        name_check = (self.__name == other.__name)
        url_check = (self.__url == other.__url)

        return name_check and url_check

    def __str__(self):
        product_name = f"Product: {self.__name}\n"
        product_img = f"Image: {self.__img_url}\n"
        product_old_price = f"Old Price: {self.__old_price}\n"
        product_price = f"Price: {self.__price}\n"
        product_dlc = f"Last checked: {self.__date_of_last_check}\n"
        product_link = f"Link: {self.__url}\n"

        return f"{product_name}{product_img}{product_old_price}{product_price}{product_dlc}{product_link}"


class ListingChange:
    def __init__(self, listing: Listing, change: Change):
        self.__listing = listing
        self.__change = change

    def get_listing(self):
        return self.__listing

    def get_change(self):
        return self.__change
