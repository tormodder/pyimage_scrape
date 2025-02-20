import requests
import sys
import logging
from bs4 import BeautifulSoup

class Scraper:
    def __init__(self, name, log_level=logging.DEBUG):
        self.name = name
        self._target = ""
        self._url = ""
        # Set up logger for this instance
        self.logger = logging.getLogger(f"Scraper-{name}")

        if not self.logger.hasHandlers():  # Avoid duplicate handlers in multiple instances
            handler = logging.StreamHandler()
            formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
            handler.setFormatter(formatter)
            self.logger.addHandler(handler)

        self.logger.setLevel(log_level)
    
    @property
    def url(self):
        return self._url

    @property
    def target(self):
        return self._target

    @target.setter
    def target(self, directory:str):
        self._target = directory

    @url.setter
    def url(self, url: str):
        self._url = url

    #private methods

    ######
    # getting links
    ######
    def __connect_and_soupify(self, url:str) -> BeautifulSoup:
        re = requests.get(url)
        if re.status_code != 200:
            logging.error("Error getting web page.")
            exit(-1)

        return BeautifulSoup(re.text, 'html.parser')


    def __get_links_from_same_domain(self, soup: BeautifulSoup, url: str) -> list[str]:
        """
        Returns only urls in the same domain
        """
        return [
            href for link in soup.find_all("a")
            if (href := link.get("href")) and (url in href) and (href != url)
        ]
    
    def __get_links_to_pictures(self, soup: BeautifulSoup, url: str) -> list[str]:
        """
        filter away links from same domain
        used to get picture links
        """
        return [
            href for link in soup.find_all("a") 
            if (href := link.get("href")) and (url not in href)
        ]

    #####
    # Page scraping
    ######
    def __scrape_one_page(self, link: str) -> tuple[str, str]:
         

        return ("", "")
            # This is where the bs4 stuff happens

    def __get_image(self, link: str) -> str:
        return ""

    def __get_image_text(self, link: str) -> str:
        return ""
    
    #TODO: Implement downloader.py
    #    def __downloader(self, text_image: tuple(str)):
        # This function should take a tuple: image and text (both strings)
        # and then download the content
        # and put it in the target folder

    #public methods
    def scrape(self):
        """
        Main method of the class
        Sould call all the other functions
        """
        soup = self.__connect_and_soupify(self.url)

        links_to_visit = self.__get_links_from_same_domain(soup, self.url)
        self.logger.info(f"Found {len(links_to_visit)} links to scrape.")

        for link in links_to_visit:
            (image, text) = self.__scrape_one_page(link)

        if self.logger.isEnabledFor(logging.DEBUG):
            for link in links_to_visit:
                self.logger.debug(f"{links_to_visit}\n")
"""
    TODO
    the program should:
        get all links to the same domain
        follow each link
        Find every picture on the page
        Download the image into target
        Save the next immediately after a picture (if any) and save to metadata
    """    
