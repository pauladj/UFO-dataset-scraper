import argparse

from exceptions import FetchingPageException
from ufo_scraper import UFOScraper


def getargs():
    """
    Create main parser.
    See program (<program> -h) helps for details.
    :return: Parsed arguments.
    """

    parser = argparse.ArgumentParser(description="UFO Scraper")

    parser.add_argument('-y', '--year', required=False, action='store',
                        help='The limit year to scrape',
                        type=int, default=1800)
    parser.add_argument('-o', '--output', required=False, action='store',
                        help='The output csv file', default="ufo_dataset.csv")

    return parser.parse_args()


args = getargs()
try:
    ufo_scraper = UFOScraper(args.year, args.output)
    ufo_scraper.scrape()
    ufo_scraper.save_to_file()
except FetchingPageException as f:
    print(f)
except Exception as e:
    print("An unexpected error ocurred: {}".format(e))
