"""
Module for scraping the web site and gathering URLs
"""
from bs4 import BeautifulSoup
import requests
import sys

def get_all_links(url: str) -> list[str]:
    re = requests.get(url)
    if re.status_code != 200:
        sys.stderr.write("Error getting web page.")
        exit(-1)

    soup = BeautifulSoup(re.text, 'html.parser')

    return [
        href for link in soup.find_all("a")
        if (href := link.get("href")) and url in href and href != url
    ]
