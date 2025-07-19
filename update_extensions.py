import json
import scraper
from sklearn.cluster import KMeans
from sklearn.feature_extraction.text import CountVectorizer


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
        self.extensions_data = self.extensions_ref_data

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
        for i, label in enumerate(kmeans.labels_):
            if label not in clusters:
                clusters[label] = []
            if i < len(self.extensions_ref_data["methods"]):
                clusters[label].append(
                    list(self.extensions_ref_data["methods"].keys())[i]
                )
            else:
                clusters[label].append(
                    list(self.extensions_ref_data["types"].keys())[
                        i - len(self.extensions_ref_data["methods"])
                    ]
                )

        print("Clusters:")
        for label, items in clusters.items():
            print(f"- Cluster {label}: {', '.join(items)}")


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
