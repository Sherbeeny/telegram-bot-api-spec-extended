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


def get_ref(element, url):
    """Extracts the reference from a BeautifulSoup element."""
    if not element:
        return None
    header = element.find_previous(["h3", "h4"])
    if not header:
        return None
    anchor = header.find("a", {"name": True})
    if not anchor:
        return None

    # Clean up the text to remove extra whitespace and newlines
    text = " ".join(element.get_text().split())

    return {
        "url": f"{url}#{anchor['name']}",
        "text": text,
    }


def scrape_faq(soup):
    """Scrapes all questions and answers from the FAQ page."""
    faq = {}
    url = "https://core.telegram.org/bots/faq"
    for h4 in soup.find_all("h4"):
        anchor = h4.find("a", {"name": True})
        if not anchor:
            continue
        question = anchor.get("name")
        if not question:
            continue

        answer = ""
        for sibling in h4.find_next_siblings():
            if sibling.name == "h4":
                break
            answer += sibling.get_text() + "\n"

        faq[question] = {
            "question": h4.get_text(),
            "answer": answer.strip(),
            "ref": get_ref(h4, url),
        }
    return {"faq": faq}


def scrape_methods(soup):
    """Scrapes method information from the API page."""
    methods = {}
    url = "https://core.telegram.org/bots/api"
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
                "ref": get_ref(h4, url),
            }
    return methods


def scrape_features(soup):
    """Scrapes all sections from the features page."""
    features = {}
    url = "https://core.telegram.org/bots/features"
    for h4 in soup.find_all("h4"):
        anchor = h4.find("a", {"name": True})
        if not anchor:
            continue
        feature_name = anchor.get("name")
        if not feature_name:
            continue

        description = ""
        for sibling in h4.find_next_siblings():
            if sibling.name == "h4":
                break
            description += sibling.get_text() + "\n"

        features[feature_name] = {
            "title": h4.get_text(),
            "description": description.strip(),
            "ref": get_ref(h4, url),
        }
    return {"features": features}


def scrape_types(soup):
    """Scrapes type information from the API page."""
    types = {}
    url = "https://core.telegram.org/bots/api"
    types_section = soup.find("h3", {"id": "available-types"})
    if types_section:
        for h4 in types_section.find_next_siblings("h4"):
            anchor = h4.find("a", {"name": True})
            if not anchor:
                continue
            type_name = anchor.get("name")
            if not type_name:
                continue

            description = ""
            for p in h4.find_next_siblings("p"):
                if p.find_previous_sibling("h4") != h4:
                    break
                description += p.get_text() + "\n"

            fields = []
            table = h4.find_next_sibling("table")
            if table:
                for tr in table.find_all("tr")[1:]:
                    tds = tr.find_all("td")
                    if len(tds) == 3:
                        fields.append(
                            {
                                "name": tds[0].get_text(),
                                "type": tds[1].get_text(),
                                "description": tds[2].get_text(),
                            }
                        )
            types[type_name] = {
                "description": description.strip(),
                "fields": fields,
                "ref": get_ref(h4, url),
            }
    return types


def scrape_all():
    """
    Scrapes all the documentation pages and returns a combined dictionary.
    """
    data = {}
    faq_url = "https://core.telegram.org/bots/faq"
    features_url = "https://core.telegram.org/bots/features"
    api_url = "https://core.telegram.org/bots/api"

    faq_soup = get_soup(faq_url)
    if faq_soup:
        data.update(scrape_faq(faq_soup))

    features_soup = get_soup(features_url)
    if features_soup:
        data.update(scrape_features(features_soup))

    api_soup = get_soup(api_url)
    if api_soup:
        data["methods"] = scrape_methods(api_soup)
        data["types"] = scrape_types(api_soup)

    return data
