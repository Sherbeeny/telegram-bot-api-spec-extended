import unittest
from unittest.mock import patch, MagicMock
import scraper


class TestScraper(unittest.TestCase):
    def test_import(self):
        self.assertIsNotNone(scraper)

    def test_scrape_all(self):
        data = scraper.scrape_all()
        self.assertIsInstance(data, dict)

    @patch("requests.get")
    def test_get_soup_error(self, mock_get):
        mock_get.side_effect = scraper.requests.exceptions.RequestException
        self.assertIsNone(scraper.get_soup("http://example.com"))

    def test_scrape_features_page(self):
        data = scraper.scrape_features_page()
        self.assertIsInstance(data, dict)

    @patch("scraper.get_soup")
    def test_scrape_api_page_no_soup(self, mock_get_soup):
        mock_get_soup.return_value = None
        self.assertEqual(scraper.scrape_api_page(), {})

    @patch("scraper.get_soup")
    def test_scrape_faq_page_no_soup(self, mock_get_soup):
        mock_get_soup.return_value = None
        self.assertEqual(scraper.scrape_faq_page(), {})

    @patch("scraper.get_soup")
    def test_scrape_features_page_no_soup(self, mock_get_soup):
        mock_get_soup.return_value = None
        self.assertEqual(scraper.scrape_features_page(), {})

    @patch("scraper.get_soup")
    def test_scrape_api_page_no_tbody(self, mock_get_soup):
        mock_soup = MagicMock()
        mock_table = MagicMock()
        mock_table.find.return_value = None
        mock_soup.find_all.return_value = [MagicMock()]
        mock_soup.find.return_value = "method"
        mock_soup.find_next_sibling.return_value = mock_table
        mock_get_soup.return_value = mock_soup
        scraper.scrape_api_page()

    @patch("scraper.get_soup")
    def test_scrape_api_page_no_method_name_anchor(self, mock_get_soup):
        mock_soup = MagicMock()
        mock_h4 = MagicMock()
        mock_h4.find.return_value = None
        mock_soup.find_all.return_value = [mock_h4]
        mock_get_soup.return_value = mock_soup
        self.assertEqual(scraper.scrape_api_page(), {})

    @patch("builtins.print")
    @patch("requests.get")
    def test_get_soup_print_error(self, mock_get, mock_print):
        mock_get.side_effect = scraper.requests.exceptions.RequestException(
            "Test error"
        )
        scraper.get_soup("http://example.com")
        mock_print.assert_called_with("Error fetching http://example.com: Test error")

    @patch("scraper.get_soup")
    def test_scrape_api_page_uppercase_method_name(self, mock_get_soup):
        mock_soup = MagicMock()
        mock_h4 = MagicMock()
        mock_h4.find.return_value = True
        mock_h4.get_text.return_value = "Method"
        mock_soup.find_all.return_value = [mock_h4]
        mock_get_soup.return_value = mock_soup
        self.assertEqual(scraper.scrape_api_page(), {})
