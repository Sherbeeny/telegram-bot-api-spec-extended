import json
import scraper
from sklearn.cluster import KMeans
from sklearn.feature_extraction.text import CountVectorizer
import datetime
import pytz


def get_cairo_time():
    """Returns the current time in Cairo timezone."""
    return datetime.datetime.now(pytz.timezone("Africa/Cairo")).isoformat()


class Generator:
    def __init__(self):
        self.scraped_data = scraper.scrape_all()
        self.extensions_ref_data = {}
        self.extensions_data = {}
        self.previous_extensions_data = self.load_previous_extensions_data()

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

        # Create copies of the data to avoid modifying the originals
        previous_data = self.previous_extensions_data.copy()
        current_data = self.extensions_data.copy()

        # Remove the timestamp fields for comparison
        previous_data.pop("x-last-check", None)
        previous_data.pop("x-last-edit", None)
        current_data.pop("x-last-check", None)
        current_data.pop("x-last-edit", None)

        return previous_data != current_data


class AIComponent:
    def __init__(self, extensions_ref_data):
        self.extensions_ref_data = extensions_ref_data

    def analyze_data(self):
        """
        Analyzes the scraped data and suggests a more optimal structure for the
        extensions.ref.json file.
        """
        descriptions = []
        if "methods" in self.extensions_ref_data:
            for method in self.extensions_ref_data["methods"].values():
                descriptions.append(method["description"])
        if "types" in self.extensions_ref_data:
            for type in self.extensions_ref_data["types"].values():
                descriptions.append(type["description"])
        if "faq" in self.extensions_ref_data:
            for question in self.extensions_ref_data["faq"].values():
                descriptions.append(question["answer"])
        if "features" in self.extensions_ref_data:
            for feature in self.extensions_ref_data["features"].values():
                descriptions.append(feature["description"])

        if not descriptions:
            print("No data to analyze.")
            return

        vectorizer = CountVectorizer(stop_words="english")
        X = vectorizer.fit_transform(descriptions)

        kmeans = KMeans(n_clusters=2, random_state=0, n_init="auto")
        kmeans.fit(X)

        clusters = {}
        methods_len = len(self.extensions_ref_data.get("methods", {}))
        types_len = len(self.extensions_ref_data.get("types", {}))
        faq_len = len(self.extensions_ref_data.get("faq", {}))
        features_len = len(self.extensions_ref_data.get("features", {}))

        for i, label in enumerate(kmeans.labels_):
            if label not in clusters:
                clusters[label] = []

            if i < methods_len:
                clusters[label].append(
                    list(self.extensions_ref_data["methods"].keys())[i]
                )
            elif i < methods_len + types_len:
                clusters[label].append(
                    list(self.extensions_ref_data["types"].keys())[i - methods_len]
                )
            elif i < methods_len + types_len + faq_len:
                clusters[label].append(
                    list(self.extensions_ref_data["faq"].keys())[
                        i - methods_len - types_len
                    ]
                )
            elif i < methods_len + types_len + faq_len + features_len:
                clusters[label].append(
                    list(self.extensions_ref_data["features"].keys())[
                        i - methods_len - types_len - faq_len
                    ]
                )

        return {str(k): v for k, v in clusters.items()}


def main():
    """
    Scrapes the Telegram Bot API documentation, generates the extensions data,
    and saves it to the extensions.json and extensions.min.json files.
    """
    generator = Generator()
    generator.generate_extensions_ref_data()
    generator.save_extensions_ref_file()

    ai_component = AIComponent(generator.extensions_ref_data)
    clusters = ai_component.analyze_data()

    generator.extensions_data = {"clusters": clusters}
    generator.save_extensions_file()


if __name__ == "__main__":
    main()
