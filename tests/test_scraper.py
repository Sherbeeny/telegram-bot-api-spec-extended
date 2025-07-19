import unittest
from bs4 import BeautifulSoup
import scraper


class TestScraper(unittest.TestCase):
    def test_get_ref(self):
        html = """
        <div>
            <h4><a name="test_anchor">Test Anchor</a></h4>
            <p>This is the text to be highlighted.</p>
        </div>
        """
        soup = BeautifulSoup(html, "html.parser")
        element = soup.find("p")
        ref = scraper.get_ref(element, "http://test.com")
        expected_ref = {
            "url": "http://test.com#test_anchor",
            "text": "This is the text to be highlighted.",
        }
        self.assertEqual(ref, expected_ref)

    def test_scrape_faq(self):
        html = """
        <div>
            <h4><a name="faq_question_1">FAQ Question 1</a></h4>
            <p>This is the answer to question 1.</p>
            <h4><a name="faq_question_2">FAQ Question 2</a></h4>
            <p>This is the answer to question 2.</p>
        </div>
        """
        soup = BeautifulSoup(html, "html.parser")
        faq = scraper.scrape_faq(soup)
        self.assertIn("faq", faq)
        self.assertIn("faq_question_1", faq["faq"])
        self.assertEqual(faq["faq"]["faq_question_1"]["question"], "FAQ Question 1")
        self.assertIn("ref", faq["faq"]["faq_question_1"])

    def test_scrape_features(self):
        html = """
        <div>
            <h4><a name="feature_1">Feature 1</a></h4>
            <p>This is the description of feature 1.</p>
            <h4><a name="feature_2">Feature 2</a></h4>
            <p>This is the description of feature 2.</p>
        </div>
        """
        soup = BeautifulSoup(html, "html.parser")
        features = scraper.scrape_features(soup)
        self.assertIn("features", features)
        self.assertIn("feature_1", features["features"])
        self.assertEqual(features["features"]["feature_1"]["title"], "Feature 1")
        self.assertIn("ref", features["features"]["feature_1"])

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
        methods = scraper.scrape_methods(soup)
        self.assertIn("getMe", methods)
        self.assertIn("ref", methods["getMe"])

    def test_scrape_types(self):
        html = """
        <div>
            <h3 id="available-types">Available types</h3>
            <h4><a name="user">User</a></h4>
            <p>This object represents a Telegram user or bot.</p>
            <table>
                <tbody>
                    <tr>
                        <th>Field</th>
                        <th>Type</th>
                        <th>Description</th>
                    </tr>
                    <tr>
                        <td>id</td>
                        <td>Integer</td>
                        <td>Unique identifier for this user or bot.</td>
                    </tr>
                </tbody>
            </table>
        </div>
        """
        soup = BeautifulSoup(html, "html.parser")
        types = scraper.scrape_types(soup)
        self.assertIn("user", types)
        self.assertIn("ref", types["user"])


if __name__ == "__main__":
    unittest.main()
