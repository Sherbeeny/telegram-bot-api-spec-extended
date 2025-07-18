import requests
from bs4 import BeautifulSoup


def get_soup(url):
    """Fetches the content of a URL and returns a BeautifulSoup object."""
    try:
        response = requests.get(url)
        response.raise_for_status()
        return BeautifulSoup(response.text, "html.parser")
    except requests.exceptions.RequestException:
        return None


def get_ref(element):
    """Extracts the reference from a BeautifulSoup element."""
    if not element:
        return None
    header = element.find_previous("h4")
    if not header:
        return None
    anchor = header.find("a", {"name": True})
    if not anchor:
        return None
    return {
        "url": f"https://core.telegram.org/bots/faq#{anchor['name']}",
        "text": element.get_text(),
    }


def scrape_rate_limits(soup):
    """Scrapes rate limit information from the FAQ page."""
    rate_limits = {}
    limit_section = soup.find(string="My bot is hitting limits, how do I avoid this?")
    if limit_section:
        ul = limit_section.find_parent("h4").find_next_sibling("ul")
        if ul:
            for li in ul.find_all("li"):
                text = li.get_text()
                if "one message per second" in text:
                    rate_limits["per_chat_per_second"] = {
                        "value": 1,
                        "ref": get_ref(li),
                    }
                if "20 messages per minute" in text:
                    rate_limits["group_per_minute"] = {
                        "value": 20,
                        "ref": get_ref(li),
                    }
                if "30 messages per second" in text:
                    rate_limits["broadcast_per_second"] = {
                        "value": 30,
                        "ref": get_ref(li),
                    }
    return {"x-rate-limit": rate_limits}


def scrape_file_size_limits(soup):
    """Scrapes file size limit information from the FAQ page."""
    file_size_limits = {}
    file_size_section = soup.find(string="How do I upload a large file?")
    if file_size_section:
        p = file_size_section.find_parent("h4").find_next_sibling("p")
        if p:
            text = p.get_text()
            if "50 MB" in text:
                file_size_limits["upload_mb"] = {
                    "value": 50,
                    "ref": get_ref(p),
                }

    file_size_section = soup.find(string="How do I download files?")
    if file_size_section:
        p = file_size_section.find_parent("h4").find_next_sibling("p")
        if p:
            text = p.get_text()
            if "20 MB" in text:
                file_size_limits["download_mb"] = {
                    "value": 20,
                    "ref": get_ref(p),
                }

    return {"x-file-size-limits": file_size_limits}


def scrape_methods(soup):
    """Scrapes method information from the API page."""
    methods = {}
    methods_section = soup.find("h3", {"id": "available-methods"})
    if methods_section:
        for h4 in methods_section.find_next_siblings("h4"):
            anchor = h4.find("a", {"name": True})
            if not anchor:
                continue
            method_name = anchor.get("name")
            if not method_name:
                continue

            description = ""
            for p in h4.find_next_siblings("p"):
                if p.find_previous_sibling("h4") != h4:
                    break
                description += p.get_text() + "\n"

            parameters = []
            table = h4.find_next_sibling("table")
            if table:
                for tr in table.find_all("tr")[1:]:
                    tds = tr.find_all("td")
                    if len(tds) == 4:
                        parameters.append(
                            {
                                "name": tds[0].get_text(),
                                "type": tds[1].get_text(),
                                "required": tds[2].get_text(),
                                "description": tds[3].get_text(),
                            }
                        )
            methods[method_name] = {
                "description": description.strip(),
                "parameters": parameters,
            }
    return methods


def scrape_features(soup):
    """Scrapes feature information from the features page."""
    features = {}
    features_section = soup.find("h3", {"id": "what-features-do-bots-have"})
    if features_section:
        for h4 in features_section.find_next_siblings("h4"):
            anchor = h4.find("a", {"name": True})
            if not anchor:
                continue
            feature_name = anchor.get("name")
            if not feature_name:
                continue

            description = ""
            for p in h4.find_next_siblings("p"):
                if p.find_previous_sibling("h4") != h4:
                    break
                description += p.get_text() + "\n"

            features[feature_name] = {"description": description.strip()}
    return features


def scrape_all():
    """
    Scrapes all the documentation pages and returns a combined dictionary.
    """
    data = {}
    faq_soup = get_soup("https://core.telegram.org/bots/faq")
    if faq_soup:
        data.update(scrape_rate_limits(faq_soup))
        data.update(scrape_file_size_limits(faq_soup))

    api_soup = get_soup("https://core.telegram.org/bots/api")
    if api_soup:
        data["methods"] = scrape_methods(api_soup)

    features_soup = get_soup("https://core.telegram.org/bots/features")
    if features_soup:
        data["features"] = scrape_features(features_soup)

    return data
