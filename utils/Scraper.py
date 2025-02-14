class Scraper:
    def __init__(self, name):
        self.name = name
        # Add attributes to init
        # self._private = ???
    
    @property
    def url(self)
        return self._url

    @property
        target(self)
            return self._target

    @target.setter
    def target(self, directory:str):
        self_target = directory

    @url.setter
    def url(self, url: str):
        self._url = value

    #private methods

    ######
    # getting links
    ######
    def __get_all_links(self, url: str) -> list[str]:
    re = requests.get(url)
    if re.status_code != 200:
        sys.stderr.write("Error getting web page.")
        exit(-1)

    soup = BeautifulSoup(re.text, 'html.parser')

    return __get_links_from_same_domain(soup)

    def __get_links_from_same_domain(self, soup: BeautifulSoup) -> list[str]:
    """
    Returns only urls in the same domain
    """
    return [
        href for link in soup.find_all("a")
        if (href := link.get("href")) and (url in href) and (href != url)
    ]
    
    def __get_links_from_different_domain(self, soup: BeautifulSoup) -> list[str]:
    """
    filter away links from same domain
    """
    return [
        href for link in soup.find_all("a") 
        if (href := link.get("href")) and (url not in href)
    ]

    #####
    # Page scraping
    ######
    def __scrape_one_page(self, links: list[str]) -> tuple(str):
        for link in links:
            # This is where the bs4 stuff happens

    def __get_image(self, link: str) -> str:

    def __get_image_text(self, link: str) -> str:
    
    #TODO: Implement downloader.py
    def __downloader(self, text_image: tuple(str)):
        # This function should take a tuple: image and text (both strings)
        # and then download the content
        # and put it in the target folder

    #public methods
    def scrape(self):
        (image, text) self.__scrape_one_page(self.__get_all_links(self.url))


    """
    TODO
    the program should:
        get all links to the same domain
        follow each link
        Find every picture on the page
        Download the image into target
        Save the next immediately after a picture (if any) and save to metadata
    """    