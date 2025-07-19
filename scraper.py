"""
This module contains functions for scraping the Telegram Bot API documentation.
"""

import requests
from bs4 import BeautifulSoup


def get_soup(url):
    """
    Fetches the content of a URL and returns a BeautifulSoup object.

    Args:
        url (str): The URL to fetch.

    Returns:
        BeautifulSoup: A BeautifulSoup object representing the parsed HTML,
                       or None if the request fails.
    """
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for bad status codes
        return BeautifulSoup(response.text, "html.parser")
    except requests.exceptions.RequestException as e:
        print(f"Error fetching {url}: {e}")
        return None


def get_ref(element, url):
    """
    Extracts the reference from a BeautifulSoup element.

    The reference consists of the URL of the page, the anchor of the
    relevant section, and the highlighted text.

    Args:
        element (bs4.element.Tag): The BeautifulSoup element to extract the
                                   reference from.
        url (str): The URL of the page.

    Returns:
        dict: A dictionary containing the reference information, or None if
              the reference cannot be extracted.
    """
    if not element:
        return None
    # Find the nearest preceding h3 or h4 tag, which represents the section header
    header = element.find_previous(["h3", "h4"])
    if not header:
        return None
    # Find the anchor tag within the header
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
    """
    Scrapes all questions and answers from the FAQ page.

    Args:
        soup (BeautifulSoup): A BeautifulSoup object representing the parsed
                              HTML of the FAQ page.

    Returns:
        dict: A dictionary containing the scraped FAQ data.
    """
    faq = {}
    url = "https://core.telegram.org/bots/faq"
    # Find all h4 tags, which represent the questions
    for h4 in soup.find_all("h4"):
        # Find the anchor tag within the h4 tag
        anchor = h4.find("a", {"name": True})
        if not anchor:
            continue
        question = anchor.get("name")
        if not question:
            continue

        # The answer is the text of all siblings until the next h4 tag
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
    """
    Scrapes method information from the API page.

    Args:
        soup (BeautifulSoup): A BeautifulSoup object representing the parsed
                              HTML of the API page.

    Returns:
        dict: A dictionary containing the scraped method data.
    """
    methods = {}
    url = "https://core.telegram.org/bots/api"
    # Find the "Available methods" section
    methods_section = soup.find("h3", {"id": "available-methods"})
    if methods_section:
        # Find all h4 tags, which represent the methods
        for h4 in methods_section.find_next_siblings("h4"):
            # Find the anchor tag within the h4 tag
            anchor = h4.find("a", {"name": True})
            if not anchor:
                continue
            method_name = anchor.get("name")
            if not method_name:
                continue

            # The description is the text of all p tags until the next h4 tag
            description = ""
            for p in h4.find_next_siblings("p"):
                if p.find_previous_sibling("h4") != h4:
                    break
                description += p.get_text() + "\n"

            # The parameters are in the table that follows the h4 tag
            parameters = []
            table = h4.find_next_sibling("table")
            if table:
                # The first row is the header, so we skip it
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
    """
    Scrapes all sections from the features page.

    Args:
        soup (BeautifulSoup): A BeautifulSoup object representing the parsed
                              HTML of the features page.

    Returns:
        dict: A dictionary containing the scraped features data.
    """
    features = {}
    url = "https://core.telegram.org/bots/features"
    # Find all h4 tags, which represent the features
    for h4 in soup.find_all("h4"):
        # Find the anchor tag within the h4 tag
        anchor = h4.find("a", {"name": True})
        if not anchor:
            continue
        feature_name = anchor.get("name")
        if not feature_name:
            continue

        # The description is the text of all siblings until the next h4 tag
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
    """
    Scrapes type information from the API page.

    Args:
        soup (BeautifulSoup): A BeautifulSoup object representing the parsed
                              HTML of the API page.

    Returns:
        dict: A dictionary containing the scraped type data.
    """
    types = {}
    url = "https://core.telegram.org/bots/api"
    # Find the "Available types" section
    types_section = soup.find("h3", {"id": "available-types"})
    if types_section:
        # Find all h4 tags, which represent the types
        for h4 in types_section.find_next_siblings("h4"):
            # Find the anchor tag within the h4 tag
            anchor = h4.find("a", {"name": True})
            if not anchor:
                continue
            type_name = anchor.get("name")
            if not type_name:
                continue

            # The description is the text of all p tags until the next h4 tag
            description = ""
            for p in h4.find_next_siblings("p"):
                if p.find_previous_sibling("h4") != h4:
                    break
                description += p.get_text() + "\n"

            # The fields are in the table that follows the h4 tag
            fields = []
            table = h4.find_next_sibling("table")
            if table:
                # The first row is the header, so we skip it
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

    Returns:
        dict: A dictionary containing all the scraped data.
    """
    data = {}
    faq_url = "https://core.telegram.org/bots/faq"
    features_url = "https://core.telegram.org/bots/features"
    api_url = "https://core.telegram.org/bots/api"

    # Scrape the FAQ page
    faq_soup = get_soup(faq_url)
    if faq_soup:
        data.update(scrape_faq(faq_soup))

    # Scrape the features page
    features_soup = get_soup(features_url)
    if features_soup:
        data.update(scrape_features(features_soup))

    # Scrape the API page
    api_soup = get_soup(api_url)
    if api_soup:
        data["methods"] = scrape_methods(api_soup)
        data["types"] = scrape_types(api_soup)

    return data
