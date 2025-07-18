import unittest
from unittest.mock import patch, MagicMock
from bs4 import BeautifulSoup
import scraper


class TestScraper(unittest.TestCase):
    @patch("scraper.get_soup")
    def test_scrape_rate_limits(self, mock_get_soup):
        mock_soup = MagicMock()
        mock_anchor = MagicMock()
        mock_anchor.__getitem__.return_value = (
            "my-bot-is-hitting-limits-how-do-i-avoid-this"
        )
        mock_header = MagicMock()
        mock_header.find.return_value = mock_anchor
        mock_li = MagicMock()
        mock_li.find_previous.return_value = mock_header
        mock_li.get_text.return_value = "more than one message per second"
        mock_ul = MagicMock()
        mock_ul.find_all.return_value = [mock_li]
        mock_limit_section = MagicMock()
        mock_limit_section.find_parent.return_value.find_next_sibling.return_value = (
            mock_ul
        )
        mock_soup.find.return_value = mock_limit_section
        mock_get_soup.return_value = mock_soup

        expected_data = {
            "x-rate-limit": {
                "per_chat_per_second": {
                    "value": 1,
                    "ref": {
                        "url": "https://core.telegram.org/bots/faq#my-bot-is-hitting-limits-how-do-i-avoid-this",
                        "text": "more than one message per second",
                    },
                }
            }
        }
        self.assertEqual(scraper.scrape_rate_limits(mock_soup), expected_data)

    @patch("scraper.get_soup")
    def test_scrape_file_size_limits(self, mock_get_soup):
        mock_soup = MagicMock()
        mock_upload_anchor = MagicMock()
        mock_upload_anchor.__getitem__.return_value = "how-do-i-upload-a-large-file"
        mock_upload_header = MagicMock()
        mock_upload_header.find.return_value = mock_upload_anchor
        mock_upload_p = MagicMock()
        mock_upload_p.find_previous.return_value = mock_upload_header
        mock_upload_p.get_text.return_value = "50 MB"
        mock_upload_section = MagicMock()
        mock_upload_section.find_parent.return_value.find_next_sibling.return_value = (
            mock_upload_p
        )

        mock_download_anchor = MagicMock()
        mock_download_anchor.__getitem__.return_value = "how-do-i-download-files"
        mock_download_header = MagicMock()
        mock_download_header.find.return_value = mock_download_anchor
        mock_download_p = MagicMock()
        mock_download_p.find_previous.return_value = mock_download_header
        mock_download_p.get_text.return_value = "20 MB"
        mock_download_section = MagicMock()
        mock_download_section.find_parent.return_value.find_next_sibling.return_value = (
            mock_download_p
        )

        def find_side_effect(string):
            if string == "How do I upload a large file?":
                return mock_upload_section
            if string == "How do I download files?":
                return mock_download_section
            return None

        mock_soup.find.side_effect = find_side_effect
        mock_get_soup.return_value = mock_soup

        expected_data = {
            "x-file-size-limits": {
                "upload_mb": {
                    "value": 50,
                    "ref": {
                        "url": "https://core.telegram.org/bots/faq#how-do-i-upload-a-large-file",
                        "text": "50 MB",
                    },
                },
                "download_mb": {
                    "value": 20,
                    "ref": {
                        "url": "https://core.telegram.org/bots/faq#how-do-i-download-files",
                        "text": "20 MB",
                    },
                },
            }
        }
        self.assertEqual(scraper.scrape_file_size_limits(mock_soup), expected_data)

    def test_scrape_methods(self):
        html = """
        <div>
            <h3 id="available-methods">Available methods</h3>
            <h4><a name="getMe">getMe</a></h4>
            <p>A simple method for testing your bot's authentication token.</p>
            <table>
                <tbody>
                    <tr>
                        <th>Parameter</th>
                        <th>Type</th>
                        <th>Required</th>
                        <th>Description</th>
                    </tr>
                    <tr>
                        <td>user_id</td>
                        <td>Integer</td>
                        <td>Yes</td>
                        <td>Unique identifier of the target user</td>
                    </tr>
                </tbody>
            </table>
        </div>
        """
        soup = BeautifulSoup(html, "html.parser")
        expected_data = {
            "getMe": {
                "description": "A simple method for testing your bot's authentication token.",
                "parameters": [
                    {
                        "name": "user_id",
                        "type": "Integer",
                        "required": "Yes",
                        "description": "Unique identifier of the target user",
                    }
                ],
            }
        }
        self.assertEqual(scraper.scrape_methods(soup), expected_data)

    def test_scrape_features(self):
        html = """
        <div>
            <h3 id="what-features-do-bots-have">What features do bots have?</h3>
            <h4><a name="inputs">Inputs</a></h4>
            <p>Users can send messages of all types to bots, including text, files, locations, stickers, voice messages and even dice if they're feeling lucky.</p>
        </div>
        """
        soup = BeautifulSoup(html, "html.parser")
        expected_data = {
            "inputs": {
                "description": "Users can send messages of all types to bots, including text, files, locations, stickers, voice messages and even dice if they're feeling lucky.",
            }
        }
        self.assertEqual(scraper.scrape_features(soup), expected_data)


if __name__ == "__main__":
    unittest.main()
