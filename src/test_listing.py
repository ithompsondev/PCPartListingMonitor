import unittest
from listing import Listing

TEST_PRODUCT = Listing().title("TEST PRODUCT").link("https://www.testlink.com")
OTHER_TEST_PRODUCT = Listing().title("OTHER TEST PRODUCT").link("https://othertestlink.com")


class TestListingEquality(unittest.TestCase):
    def test_equality_for_the_same_product(self):
        self.assertEqual(TEST_PRODUCT, TEST_PRODUCT)

    def test_equality_for_different_products(self):
        self.assertNotEqual(TEST_PRODUCT, OTHER_TEST_PRODUCT)


unittest.main()
