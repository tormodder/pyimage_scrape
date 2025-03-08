import requests
import sys
import logging
import os
from bs4 import BeautifulSoup
from bs4 import XMLParsedAsHTMLWarning
import warnings

warnings.filterwarnings("ignore", category=XMLParsedAsHTMLWarning)
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
        elif re.text.startswith("<?xml"):
            logging.error("Page is xml. Skipping...")
            return None

        soup = BeautifulSoup(re.text, 'html.parser')

        return soup


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

        soup = self.__connect_and_soupify(link)
        if not soup:
            self.logger.error("xml skpped from scraper function")
            return ("", "")
    
        img = self.__get_links_to_pictures(soup, link)

         #TODO find subsequent text
         #      store subsequent text
        txt = ""

        return (img, txt)

    
    #TODO: Implement downloader.py
    def __downloader(self, text_image: tuple[str, str]):
        img = text_image[0]
        txt = text_image[1]

        if not img and not txt:
            self.logger.error("No image or text found.")
            return
        
        # Remove when txt is found
        file_name = os.path.basename(img)
        file_path = os.path.join(self.target, file_name)

        self.logger.info(f"Downloading file {file_name}")
        
        img_data = requests.get(img).content
        with open(file_path, "wb") as f:
            f.write(img_data)




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
            if self.logger.isEnabledFor(logging.DEBUG):
                self.logger.debug(f"{link}\n")

           # (image, text) = self.__scrape_one_page(link)
            self.__downloader(self.__scrape_one_page(link))


"""
    TODO
    the program should:
        get all links to the same domain
        follow each link
        Find every picture on the page
        Download the image into target
        Save the next immediately after a picture (if any) and save to metadata
    """    
