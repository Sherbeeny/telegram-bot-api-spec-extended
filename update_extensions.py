import json
import scraper


def get_key_methods(scraped_data):
    """
    Returns a list of key methods to include in the extensions file.
    """
    key_methods = [
        "sendMessage",
        "sendPhoto",
        "editMessageText",
        "answerCallbackQuery",
        "getUpdates",
    ]
    return [method for method in key_methods if method in scraped_data]


def generate_extensions_data(scraped_data, key_methods):
    """
    Generates the extensions data for the given methods.
    """
    extensions_data = {}
    for method_name in key_methods:
        extensions_data[method_name] = {}
        if "x-rate-limit" in scraped_data.get(method_name, {}):
            extensions_data[method_name]["x-rate-limit"] = (
                scraped_data[method_name]["x-rate-limit"]
            )
    return extensions_data


def save_extensions_file(extensions_data):
    """
    Saves the extensions data to extensions.json and extensions.min.json.
    """
    with open("extensions.json", "w") as f:
        json.dump(extensions_data, f, indent=2)

    with open("extensions.min.json", "w") as f:
        json.dump(extensions_data, f, separators=(",", ":"))


def main():
    """
    Scrapes the Telegram Bot API documentation, generates the extensions data,
    and saves it to the extensions.json and extensions.min.json files.
    """
    scraped_data = scraper.scrape_all()
    key_methods = get_key_methods(scraped_data)
    extensions_data = generate_extensions_data(scraped_data, key_methods)
    save_extensions_file(extensions_data)


if __name__ == "__main__":
    main()
