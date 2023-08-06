import unittest

from scraper import Scraper
from twitter import TwitterAuthentication


class TestSimpleScraping(unittest.TestCase):

    def testCanScrape(self):
        """Tests that scraper can scrape one term."""

        twauth = TwitterAuthentication.autodetect_twitter_auth()

        scraper = Scraper(twitter_authentication=twauth)

        scraper.scrape_terms({"potato"}, count=1)
