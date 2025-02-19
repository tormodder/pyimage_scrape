from utils.Scraper import Scraper

def main():
    target = "https://pelleohlinmorbidmayhem.blogspot.com/"
    output_dir = "output/images"
    
    scraper = Scraper("debug")
    scraper.url = target

    scraper.scrape()

if __name__ == "__main__":
    main()
