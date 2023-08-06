"""
This file demonstrates the Scraper class' ability to scrape small amounts of tweets about a simple term or hashtag, like
'pizza', '#pizza', 'cat', and '#cat', and save them to a MongoDB database.
"""
from pymongo import MongoClient

import __init__

from pprint import pprint

from config import Config
from scraper import Scraper
from twitter import GEOBOX_CHICAGO
from util import geobox_to_geocode, flatten_status_dict, save_statuses_dict_to_mongodb

if __name__ == '__main__':
    mongoclient = MongoClient(Config.DEFAULT_MONGODB_CONNECTION_STRING)

    mongodb = mongoclient['testScraperSimpleTermsPizzaSaveToMongoDB']

    scraper = Scraper()

    terms = {"#pizza", "pizza", 'cat', '#cat'}

    # Scrape results
    results = scraper.scrape_terms(geocode=geobox_to_geocode(GEOBOX_CHICAGO, "20mi"), terms=terms, count=3)

    # Save results to mongoDB
    save_statuses_dict_to_mongodb(results, mongodb, print_on_duplicates=True)

    results = flatten_status_dict(results)
    print("{} in chicago:".format(", ".join(terms)))
    pprint(results)
