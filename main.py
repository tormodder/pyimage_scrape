from utils.Scraper import Scraper

def main():
    url = "https://pelleohlinmorbidmayhem.blogspot.com/"
    output_dir = "output/images"
    
    scraper = Scraper("debug")
    scraper.url = url

    scraper.scrape()

if __name__ == "__main__":
    main()
