import csv
from bs4 import BeautifulSoup
import requests

class Scraper:
    def __init__(self, url):
        self.url = url
        self.book_title = ""
        self.product_page_url = ""
        self.universal_product_code = ""
        self.price_including_tax = ""
        self.price_excluding_tax = ""
        self.quantity_available = ""
        self.product_description = ""
        self.category = ""
        self.review_rating = ""
        self.image_url = ""

    def scrape(self):
        page = requests.get(self.url)
        doc = BeautifulSoup(page.content, "html.parser")

        # Product Page URL
        self.product_page_url = page.url

        # Universal product code
        universal_product_code_doc = doc.find_all("tr")[0]
        self.universal_product_code = universal_product_code_doc.find("td").string

        # Book Title
        self.book_title = doc.title.string.strip()

        # Price Including Tax
        price_including_tax_doc = doc.find_all("tr")[3]
        self.price_including_tax = price_including_tax_doc.find("td").string

        # Price Excluding Tax
        price_excluding_tax_doc = doc.find_all("tr")[2]
        self.price_excluding_tax = price_excluding_tax_doc.find("td").string

        # Quantity Available
        quantity_available_doc = doc.find_all("tr")[5]
        self.quantity_available = quantity_available_doc.find("td").string

        # Product Description
        product_description_doc = doc.find("article", class_="product_page")
        self.product_description = product_description_doc.find_all("p")[-1].string

        # Category
        category_doc = doc.find_all("li")[2]
        self.category = category_doc.find("a").string

        # Review Rating
        review_rating_doc = doc.find("p", class_="star-rating")
        self.review_rating = review_rating_doc.get("class")[1]

        # Image URL
        image_url_doc = doc.find("img")
        image_url_text = image_url_doc.get("src")
        self.image_url = image_url_text.replace("../..", "https://books.toscrape.com", 1)

    def csv_file(self):
        # CSV file
        headers = ["Book Title", "Product Page URL", "Universal Product Code (UPC)", "Price Including Tax",
                   "Price Excluding Tax", "Quantity Available", "Product Description", "Category", "Review Rating",
                   "Image URL"]
        columns = [self.book_title, self.product_page_url, self.universal_product_code, self.price_including_tax, self.price_excluding_tax,
                   self.quantity_available, self.product_description, self.category, self.review_rating, self.image_url]
        with open("phase1.csv", "w", newline="") as file:
            # make a writer object using the file
            writer = csv.writer(file, delimiter=",")
            # create headers and columns
            writer.writerow(headers)
            writer.writerow(columns)