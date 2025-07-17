from unittest.mock import patch, MagicMock
from scraper import (
    get_soup,
    scrape_all,
    scrape_features_page,
    scrape_api_page,
    scrape_faq_page,
)
import scraper


def test_import():
    assert scraper is not None


def test_scrape_all():
    data = scrape_all()
    assert isinstance(data, dict)


@patch("requests.get")
def test_get_soup_error(mock_get):
    mock_get.side_effect = scraper.requests.exceptions.RequestException
    assert get_soup("http://example.com") is None


def test_scrape_features_page():
    data = scrape_features_page()
    assert isinstance(data, dict)


@patch("scraper.get_soup")
def test_scrape_api_page_no_soup(mock_get_soup):
    mock_get_soup.return_value = None
    assert scrape_api_page() == {}


@patch("scraper.get_soup")
def test_scrape_faq_page_no_soup(mock_get_soup):
    mock_get_soup.return_value = None
    assert scrape_faq_page() == {}


@patch("scraper.get_soup")
def test_scrape_features_page_no_soup(mock_get_soup):
    mock_get_soup.return_value = None
    assert scrape_features_page() == {}


@patch("scraper.get_soup")
def test_scrape_api_page_no_tbody(mock_get_soup):
    mock_soup = MagicMock()
    mock_table = MagicMock()
    mock_table.find.return_value = None
    mock_soup.find_all.return_value = [MagicMock()]
    mock_soup.find.return_value = "method"
    mock_soup.find_next_sibling.return_value = mock_table
    mock_get_soup.return_value = mock_soup
    scrape_api_page()


@patch("scraper.get_soup")
def test_scrape_api_page_no_method_name_anchor(mock_get_soup):
    mock_soup = MagicMock()
    mock_h4 = MagicMock()
    mock_h4.find.return_value = None
    mock_soup.find_all.return_value = [mock_h4]
    mock_get_soup.return_value = mock_soup
    assert scrape_api_page() == {}


@patch("scraper.get_soup")
def test_scrape_api_page_uppercase_method_name(mock_get_soup):
    mock_soup = MagicMock()
    mock_h4 = MagicMock()
    mock_h4.find.return_value = True
    mock_h4.get_text.return_value = "Method"
    mock_soup.find_all.return_value = [mock_h4]
    mock_get_soup.return_value = mock_soup
    assert scrape_api_page() == {}
