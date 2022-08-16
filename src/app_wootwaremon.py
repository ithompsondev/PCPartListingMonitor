from wootwaremon import WootwareListingGenerator
from monitor import Monitor
from notify import LogDumpNotifier


def main():
    monitor = Monitor(notifier=LogDumpNotifier("Wootware Product Listing Monitor"))
    wootware = WootwareListingGenerator(monitor.load_product_listings())
    listings = wootware.parse_listings()
    monitor.save_product_listings(listings)
    monitor.monitor_changes(wootware.get_product_listings(), listings)  # requires test, mock product listings


if __name__ == "__main__":
    main()
