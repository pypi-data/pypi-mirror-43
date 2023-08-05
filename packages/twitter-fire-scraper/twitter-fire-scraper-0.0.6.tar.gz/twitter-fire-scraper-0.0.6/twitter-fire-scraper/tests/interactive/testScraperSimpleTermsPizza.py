"""
This file demonstrates the Scraper class' ability to scrape small amounts of tweets about a simple term or hashtag, like
'pizza', '#pizza', 'cat', and '#cat'.
"""

import __init__

from pprint import pprint

from scraper import Scraper
from twitter import GEOBOX_CHICAGO
from util import geobox_to_geocode, flatten_status_dict

if __name__ == '__main__':
    scraper = Scraper()

    terms = {"#pizza", "pizza", 'cat', '#cat'}

    results = scraper.scrape_terms(terms=terms, count=3)
    results = flatten_status_dict(results)

    print("{} on all of twitter:".format(", ".join(terms)))
    pprint(results)

    results = scraper.scrape_terms(geocode=geobox_to_geocode(GEOBOX_CHICAGO, "20mi"), terms=terms, count=3)
    results = flatten_status_dict(results)
    print("{} in chicago:".format(", ".join(terms)))
    pprint(results)
