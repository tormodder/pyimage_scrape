from utils.scraper import get_all_links

def main():
    target = ""
    output_dir = "output/images"
    
    links = get_all_links(target)

    for i in links:
        print(i)

if __name__ == "__main__":
    main()
