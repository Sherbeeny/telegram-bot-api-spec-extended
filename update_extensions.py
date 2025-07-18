import json
import scraper


class Generator:
    def __init__(self):
        self.scraped_data = scraper.scrape_all()
        self.extensions_ref_data = {}
        self.extensions_data = {}

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
        key_methods = [
            "sendMessage",
            "sendPhoto",
            "editMessageText",
            "answerCallbackQuery",
            "getUpdates",
        ]

        for method in key_methods:
            self.extensions_data[method] = {}

        if "x-rate-limit" in self.extensions_ref_data:
            rate_limits = {}
            for key, value in self.extensions_ref_data["x-rate-limit"].items():
                rate_limits[key] = value
            for method in self.extensions_data:
                self.extensions_data[method]["x-rate-limit"] = rate_limits

        if "x-file-size-limits" in self.extensions_ref_data:
            if "sendPhoto" in self.extensions_data:
                self.extensions_data["sendPhoto"]["x-restrictions"] = {
                    "photo": {
                        "max_size_mb": 10,
                        "max_dimensions_total": 10000,
                        "max_ratio": 20,
                    },
                    "caption": {"max_length": 1024},
                }

        if "sendMessage" in self.extensions_data:
            self.extensions_data["sendMessage"]["x-restrictions"] = {
                "text": {"max_length": 4096}
            }
        if "editMessageText" in self.extensions_data:
            self.extensions_data["editMessageText"]["x-restrictions"] = {
                "edit": {"max_age_hours": 48},
                "text": {"max_length": 4096},
            }
        if "answerCallbackQuery" in self.extensions_data:
            self.extensions_data["answerCallbackQuery"]["x-restrictions"] = {
                "text": {"max_length": 200}
            }
        if "getUpdates" in self.extensions_data:
            self.extensions_data["getUpdates"]["x-restrictions"] = {
                "limit": {"min_value": 1, "max_value": 100, "default_value": 100},
                "timeout": {"default_value": 0},
            }

    def save_extensions_file(self):
        """
        Saves the extensions data to extensions.json and extensions.min.json.
        """
        with open("extensions.json", "w") as f:
            json.dump(self.extensions_data, f, indent=2)

        with open("extensions.min.json", "w") as f:
            json.dump(self.extensions_data, f, separators=(",", ":"))


class AIComponent:
    def __init__(self, extensions_ref_data):
        self.extensions_ref_data = extensions_ref_data

    def analyze_data(self):
        """
        Analyzes the scraped data and suggests a more optimal structure for the
        extensions.ref.json file.
        """
        # TODO: Implement the AI logic here.
        pass


def main():
    """
    Scrapes the Telegram Bot API documentation, generates the extensions data,
    and saves it to the extensions.json and extensions.min.json files.
    """
    generator = Generator()
    generator.generate_extensions_ref_data()
    generator.save_extensions_ref_file()

    ai_component = AIComponent(generator.extensions_ref_data)
    ai_component.analyze_data()

    generator.generate_extensions_data_from_ref()
    generator.save_extensions_file()


if __name__ == "__main__":
    main()
