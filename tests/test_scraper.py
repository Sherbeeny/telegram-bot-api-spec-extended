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
def test_scrape_api_page_returns(mock_get_soup):
    mock_soup = MagicMock()
    mock_method = MagicMock()
    mock_method.get_text.return_value = "getMe"
    mock_description = MagicMock()
    mock_description.get_text.return_value = "On success, a User object is returned."
    mock_method.find_next_sibling.return_value = mock_description
    mock_soup.find_all.return_value = [mock_method]
    mock_get_soup.return_value = mock_soup
    data = scrape_api_page()
    assert "returns" in data["getMe"]


@patch("scraper.get_soup")
def test_scrape_faq_page_file_size_limits(mock_get_soup):
    mock_soup = MagicMock()
    mock_section = MagicMock()
    mock_ul = MagicMock()
    mock_li1 = MagicMock()
    mock_li1.get_text.return_value = "20 MB for video"
    mock_li2 = MagicMock()
    mock_li2.get_text.return_value = "50 MB for documents"
    mock_li3 = MagicMock()
    mock_li3.get_text.return_value = "10 MB for photos"
    mock_ul.find_all.return_value = [mock_li1, mock_li2, mock_li3]
    mock_parent = MagicMock()
    mock_parent.find_next_sibling.return_value = mock_ul
    mock_section.find_parent.return_value = mock_parent
    mock_soup.find.return_value = mock_section
    mock_get_soup.return_value = mock_soup
    data = scrape_faq_page()
    assert "x-file-size-limits" in data
    assert "video" in data["x-file-size-limits"]
    assert "document" in data["x-file-size-limits"]
    assert "photo" in data["x-file-size-limits"]


@patch("scraper.get_soup")
def test_scrape_features_page_with_content(mock_get_soup):
    mock_soup = MagicMock()
    mock_commands_section = MagicMock()
    mock_commands_parent = MagicMock()
    mock_commands_parent.find_next_sibling.return_value.get_text.return_value = (
        "Bot commands"
    )
    mock_commands_section.find_parent.return_value = mock_commands_parent
    mock_inline_mode_section = MagicMock()
    mock_inline_mode_parent = MagicMock()
    mock_inline_mode_parent.find_next_sibling.return_value.get_text.return_value = (
        "Inline mode"
    )
    mock_inline_mode_section.find_parent.return_value = mock_inline_mode_parent
    mock_soup.find.side_effect = [mock_commands_section, mock_inline_mode_section]
    mock_get_soup.return_value = mock_soup
    data = scrape_features_page()
    assert "x-features" in data
    assert "commands" in data["x-features"]
    assert "inline_mode" in data["x-features"]


@patch("scraper.get_soup")
def test_scrape_api_page_uppercase_method_name(mock_get_soup):
    mock_soup = MagicMock()
    mock_h4 = MagicMock()
    mock_h4.find.return_value = True
    mock_h4.get_text.return_value = "Method"
    mock_soup.find_all.return_value = [mock_h4]
    mock_get_soup.return_value = mock_soup
    assert scrape_api_page() == {}
