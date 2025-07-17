import json
import scraper

def main():
    scraped_data = scraper.scrape_all()

    key_methods = [
        "sendMessage",
        "sendPhoto",
        "editMessageText",
        "answerCallbackQuery",
        "getUpdates",
    ]

    extensions_data = {}
    for method_name in key_methods:
        if method_name in scraped_data:
            extensions_data[method_name] = {}
            if "x-rate-limit" in scraped_data[method_name]:
                extensions_data[method_name]["x-rate-limit"] = scraped_data[method_name]["x-rate-limit"]

    with open("extensions.json", "w") as f:
        json.dump(extensions_data, f, indent=2)

    with open("extensions.min.json", "w") as f:
        json.dump(extensions_data, f, separators=(",", ":"))

if __name__ == "__main__":
    main()
