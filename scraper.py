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


def scrape_all():
    """
    Scrapes all the documentation pages and returns a combined dictionary.
    """
    data = {}
    faq_soup = get_soup("https://core.telegram.org/bots/faq")
    if faq_soup:
        data.update(scrape_rate_limits(faq_soup))
        data.update(scrape_file_size_limits(faq_soup))

    return data
