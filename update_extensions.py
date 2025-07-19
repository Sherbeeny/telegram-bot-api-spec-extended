import json
import datetime
import pytz
import requests
from bs4 import BeautifulSoup

URLS = ["https://core.telegram.org/bots/faq", "https://core.telegram.org/bots/features"]


class Scraper:
    def __init__(self, urls, api_data):
        self.urls = urls
        self.api_data = api_data
        self.scraped_data = {"methods": {}, "types": {}}

    def run(self):
        """
        Runs the scraping process.
        """
        for url in self.urls:
            response = requests.get(url)
            soup = BeautifulSoup(response.content, "html.parser")
            if "faq" in url:
                self.scraped_data.update(self._parse_faq(soup))
            else:
                supplemental_data = self._parse_supplemental_data(soup)
                for method, data in supplemental_data.get("methods", {}).items():
                    if method in self.scraped_data["methods"]:
                        self.scraped_data["methods"][method].update(data)
                    else:
                        self.scraped_data["methods"][method] = data
        return self.scraped_data

    def _parse_supplemental_data(self, soup):
        """
        Parses a page for supplemental data for methods and types.
        """
        supplemental_data = {"methods": {}, "types": {}}
        return supplemental_data

    def _parse_faq(self, soup):
        """
        Parses the FAQ page.
        """
        rate_limit_text = ""
        rate_limit_value = 0

        h4_tag = soup.find(
            "a", {"name": "my-bot-is-hitting-limits-how-do-i-avoid-this"}
        )
        if h4_tag:
            for sibling in h4_tag.parent.find_next_siblings():
                if sibling.name == "h4":
                    break
                if sibling.name == "p":
                    rate_limit_text += sibling.get_text() + " "

        if "at no cost" in rate_limit_text:
            rate_limit_value = 30
        if "at a cost" in rate_limit_text:
            rate_limit_value = 1000

        return {
            "x-rate-limits": {
                "per_second": {
                    "ref": {
                        "url": "https://core.telegram.org/bots/faq#my-bot-is-hitting-limits-how-do-i-avoid-this",
                        "text": rate_limit_text.strip(),
                    },
                    "value": rate_limit_value,
                }
            }
        }


def get_cairo_time():
    """Returns the current time in Cairo timezone."""
    return datetime.datetime.now(pytz.timezone("Africa/Cairo")).isoformat()


class Generator:
    def __init__(self):
        self.api_data = self.load_api_data()
        self.scraper = Scraper(URLS, self.api_data)
        self.scraped_data = self.scraper.run()
        self.extensions_ref_data = {}
        self.extensions_data = {}
        self.previous_extensions_data = self.load_previous_extensions_data()

    def load_api_data(self):
        """Loads the api.json file."""
        try:
            with open("api.json", "r") as f:
                return json.load(f)
        except FileNotFoundError:
            return {"methods": {}, "types": {}}

    def load_previous_extensions_data(self):
        """Loads the previous extensions data from extensions.json."""
        try:
            with open("extensions.json", "r") as f:
                return json.load(f)
        except FileNotFoundError:
            return {}

    def generate_extensions_ref_data(self):
        """
        Generates the extensions reference data from the scraped data.
        """
        self.extensions_ref_data = self.scraped_data

    def save_extensions_ref_file(self):
        """
        Saves the extensions reference data to the extensions.ref.json file.
        """
        with open("extensions.ref.json", "w") as f:
            json.dump(self.extensions_ref_data, f, indent=2)

    def generate_extensions_data_from_ref(self):
        """
        Generates the extensions data from the extensions reference data.
        """
        self.extensions_data = self.extensions_ref_data

    def save_extensions_file(self):
        """
        Saves the extensions data to extensions.json and extensions.min.json.
        """
        now = get_cairo_time()
        self.extensions_data["x-last-check"] = now
        if self.extensions_data_changed():
            self.extensions_data["x-last-edit"] = now

        with open("extensions.json", "w") as f:
            json.dump(self.extensions_data, f, indent=2)

        with open("extensions.min.json", "w") as f:
            json.dump(self.extensions_data, f, separators=(",", ":"))

    def extensions_data_changed(self):
        """
        Checks if the extensions data has changed since the last run.
        """
        if not self.previous_extensions_data:
            return True

        previous_data = self.previous_extensions_data.copy()
        current_data = self.extensions_data.copy()

        previous_data.pop("x-last-check", None)
        previous_data.pop("x-last-edit", None)
        current_data.pop("x-last-check", None)
        current_data.pop("x-last-edit", None)

        return previous_data != current_data


class AIComponent:
    """
    The AIComponent class is responsible for structuring the scraped data.
    """

    def __init__(self, scraped_data, api_data):
        """
        Initializes the AIComponent.

        Args:
            scraped_data (dict): The scraped data.
            api_data (dict): The data from api.json.
        """
        self.scraped_data = scraped_data
        self.api_data = api_data

    def structure_data(self):
        """
        Structures the scraped data into the desired format, avoiding duplication.
        """
        structured_data = {"methods": {}, "types": {}}

        if "x-rate-limits" in self.scraped_data:
            structured_data["x-rate-limits"] = self.scraped_data["x-rate-limits"]

        for method_name, method_data in self.scraped_data.get("methods", {}).items():
            if method_name in self.api_data.get("methods", {}):
                for key, value in method_data.items():
                    if key.startswith("x-"):
                        if method_name not in structured_data["methods"]:
                            structured_data["methods"][method_name] = {}
                        structured_data["methods"][method_name][key] = value

        return structured_data


def main():
    """
    Scrapes the Telegram Bot API documentation, generates the extensions data,
    and saves it to the extensions.json and extensions.min.json files.
    """
    generator = Generator()
    generator.generate_extensions_ref_data()
    generator.save_extensions_ref_file()

    ai_component = AIComponent(generator.extensions_ref_data, generator.api_data)
    structured_data = ai_component.structure_data()

    generator.extensions_data = structured_data
    generator.save_extensions_file()


if __name__ == "__main__":
    main()
