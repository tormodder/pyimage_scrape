from __future__ import annotations
import requests
import sys
import logging
import os
import re
from PIL import Image
import piexif
from urllib.parse import urlparse
from urllib.request import urlopen
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
    
    def __get_links_to_pictures(self, soup: BeautifulSoup, url: str) -> list[tuple[str, str]]:
        """
        filter away links from same domain
        used to get picture links
        """
        base_domain = urlparse(url).netloc
        image_and_text = []
        
        for link in soup.select("a:has(img)"):
            href = link.get("href")
            if not href:
                continue
            if urlparse(href).netloc != base_domain:
                img_txt = self.__get_image_text(link)
                image_and_text.append((href, img_txt))
                #self.logger.debug(f"Image link: {href}\nImage text: {img_txt}")
            
        return image_and_text
        
    def __get_image_text(self, link: bs4.element.Tag) -> str:
        """
        Find the text associated with the image
        """
        text = ""

        potential_text = link.find_next(string=True)
        potential_text_test = re.sub(r'[^A-Za-z0-9]', '', potential_text.strip())
        if potential_text_test.isalnum():
            text = potential_text.strip()
    
        return text 

    #####
    # Page scraping
    ######
    def __scrape_images(self, link: str) -> tuple[list[tuple[str, str]], str]:
        """
        gets all the specified links on one single page
        """
        soup = self.__connect_and_soupify(link)
        if not soup:
            self.logger.error("xml skipped from __scrape_images")
            return "","" 
    
        pagename = soup.find("h3").text if soup.find("h3") else "" 
        self.logger.debug(f"Page name: {pagename}")
        img_txt = self.__get_links_to_pictures(soup, link)

        return (img_txt,  pagename.strip())


    def __downloader(self, text_image: list[tuple[str, str]], pagename: str) -> None:
        """
        Downloads a single image, gives it a name and stores it in the target directory
        :param text_image: tuple of (image_link, name_of_image)
        """
        counter = 0

        if not text_image:
            self.logger.error("No image or text found.")
            return 
        target_dir = self.__setup_target_directory(pagename)

        for img, text in text_image:
            self.logger.debug(f"Target directory: {target_dir}")
            
            try:
                img_data = Image.open(urlopen(img))
            except Exception as e:
                self.logger.error(f"Error opening image {img}: {e}")
                continue


            img_extension = img_data.format.lower()

            if not text:
                file_name = pagename + f"_{counter}.{img_extension}"
                counter += 1
            else:
                file_name = text + f"{img_extension}" 
            
            self.logger.info(f"Downloading file: {file_name}")
            file_path = os.path.join(target_dir, file_name)

            try: 
                img_data.save(file_path)
            except Exception as e:
                self.logger.error(f"Error downloading {img}: {e}")
                continue

    def __setup_target_directory(self, pagename: str) -> str:
        """
        Create a target directory if it doesn't exist.
        Create a subdirectory for the page name.
        :param pagename: name of the page to create a directory for
        """
        if not os.path.exists(self.target):
            os.makedirs(self.target)
            self.logger.info(f"Created target directory: {self.target}")

        # Create a subdirectory for the page name
        page_directory = os.path.join(self.target, pagename)
        if not os.path.exists(page_directory):
            os.makedirs(page_directory)
            self.logger.info(f"Created subdirectory: {page_directory}")

        return page_directory

    #public methods
    def scrape(self):
        soup = self.__connect_and_soupify(self.url)

        links_to_visit = self.__get_links_from_same_domain(soup, self.url)
        self.logger.info(f"Found {len(links_to_visit)} links to scrape.")

        # Each of the links in links_to_visit is a link to a page
        # that contains links to images
        for link in links_to_visit:
            if self.logger.isEnabledFor(logging.DEBUG):
                self.logger.debug(f"{link}\n")

            text_and_image, pagename = self.__scrape_images(link)
            self.__downloader(text_and_image, pagename)