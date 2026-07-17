from phase4 import Scraper

if __name__ == "__main__":
    url = "https://books.toscrape.com/index.html"
    scraper = Scraper(url)
    scraper.scrape()
    scraper.csv_file()
    scraper.get_image()