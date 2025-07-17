import requests
from bs4 import BeautifulSoup

def get_soup(url):
    """Fetches the content of a URL and returns a BeautifulSoup object."""
    try:
        response = requests.get(url)
        response.raise_for_status()
        return BeautifulSoup(response.text, "html.parser")
    except requests.exceptions.RequestException as e:
        print(f"Error fetching {url}: {e}")
        return None

def scrape_api_page():
    """Scrapes the main API documentation page."""
    soup = get_soup("https://core.telegram.org/bots/api")
    if not soup:
        return {}

    data = {}
    methods = soup.find_all("h4")

    for method in methods:
        method_name_anchor = method.find("a", {"name": True})
        if not method_name_anchor:
            continue
        method_name = method.get_text()

        if not method_name[0].islower():
            continue

        data[method_name] = {}

        # The description is in the next p tag
        description = method.find_next_sibling("p")
        if description:
            data[method_name]["description"] = description.get_text()

        # The parameters are in the next table
        table = method.find_next_sibling("table")
        if table:
            parameters = []
            tbody = table.find("tbody")
            if not tbody:
                continue
            for row in tbody.find_all("tr"):
                cols = row.find_all("td")
                if len(cols) == 3:
                    parameters.append(
                        {
                            "name": cols[0].get_text(),
                            "type": cols[1].get_text(),
                            "description": cols[2].get_text(),
                        }
                    )
            data[method_name]["parameters"] = parameters

    return data

def scrape_faq_page():
    """Scrapes the FAQ page."""
    soup = get_soup("https://core.telegram.org/bots/faq")
    if not soup:
        return {}

    data = {}
    # Find the "My bot is hitting limits, how do I avoid this?" section
    limit_section = soup.find(text="My bot is hitting limits, how do I avoid this?")
    if limit_section:
        # The rate limit information is in the following ul tag
        ul = limit_section.find_parent("h4").find_next_sibling("ul")
        if ul:
            for li in ul.find_all("li"):
                text = li.get_text()
                if "one message per second" in text:
                    data["global"] = {"per_second": 1}
                if "20 messages per minute" in text:
                    data["group"] = {"per_minute": 20}
                if "30 messages per second" in text:
                    data["broadcast"] = {"per_second": 30}
    return {"x-rate-limit": data}

def scrape_features_page():
    """Scrapes the features page."""
    soup = get_soup("https://core.telegram.org/bots/features")
    if not soup:
        return {}
    # Placeholder for scraping logic
    return {}

def scrape_all():
    """Scrapes all the documentation pages and returns a combined dictionary."""
    api_data = scrape_api_page()
    faq_data = scrape_faq_page()
    features_data = scrape_features_page()

    # Add the x-rate-limit data to each method
    if "x-rate-limit" in faq_data:
        for method in api_data:
            api_data[method]["x-rate-limit"] = faq_data["x-rate-limit"]

    # Add the other x- fields from the original file
    api_data["sendMessage"]["x-premium-restrictions"] = {
        "max_message_length": 8192,
        "source": "Community-tested",
    }
    api_data["sendMessage"]["x-notes"] = [
        "The general rate limit is 30 messages per second. The 20 messages per minute per chat limit is a common bottleneck.",
        "Premium users can send messages up to 8192 characters long, while non-premium users are limited to 4096.",
    ]
    api_data["sendPhoto"]["x-restrictions"] = {
        "max_file_size_mb": 10,
        "max_dimensions_total": 10000,
        "max_ratio": 20,
        "source": "https://core.telegram.org/bots/api#sendphoto",
    }
    api_data["sendPhoto"]["x-notes"] = "The photo must be at most 10 MB in size. The photo's width and height must not exceed 10000 in total. Width and height ratio must be at most 20."
    api_data["editMessageText"]["x-restrictions"] = {
        "message_age_limit_hours": 48,
        "source": "https://core.telegram.org/bots/api#editmessagetext",
    }
    api_data["editMessageText"]["x-notes"] = "A message can only be edited if it was sent less than 48 hours ago."
    api_data["answerCallbackQuery"]["x-notes"] = "The answer will be displayed to the user as a notification at the top of the chat screen or as an alert."
    api_data["getUpdates"]["x-long-polling-behavior"] = {
        "timeout_seconds": 50,
        "source": "https://core.telegram.org/bots/api#getupdates",
    }
    api_data["getUpdates"]["x-notes"] = "Long polling is used to receive incoming updates. The timeout parameter determines how long the request will wait for an update."

    return api_data
