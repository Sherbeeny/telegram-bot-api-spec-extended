import unittest
import scraper


class TestScraper(unittest.TestCase):
    def test_import(self):
        self.assertIsNotNone(scraper)

    def test_scrape_all(self):
        data = scraper.scrape_all()
        self.assertIsInstance(data, dict)


if __name__ == "__main__":
    unittest.main()
