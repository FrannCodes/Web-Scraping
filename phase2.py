import csv
from bs4 import BeautifulSoup
import requests

class Scraper:
    def __init__(self, url):
        self.url = url

        self.end_of_page = False

        self.product_page_url = []
        self.universal_product_code = []
        self.book_title = []
        self.price_including_tax = []
        self.price_excluding_tax = []
        self.product_description = []
        self.category = []
        self.review_rating = []
        self.image_url = []
        self.quantity_available = []

    def get_urls(self):
        # a loop that checks all products until the end of page
        while not self.end_of_page:
            # declare objects and variables within loop so it can be changed
            page = requests.get(self.url)
            doc = BeautifulSoup(page.content, "html.parser")

            next_page = doc.find("li", class_="next")

            product_page_url_doc = doc.find_all("div", class_="image_container")  # gets a list of elements which contains the links of the books
            for p in product_page_url_doc:
                # finds a string of elements with the tag "a"
                product = p.find("a")
                # add product page urls to an array of product_page_url:
                self.product_page_url.append(product.get("href").replace("../../..", "https://books.toscrape.com/catalogue", 1))
            if next_page is None:
                self.end_of_page = True
            else:
                url_section = next_page.find("a").get("href")
                self.url = "https://books.toscrape.com/catalogue/category/books/fantasy_19/" + url_section

    def scrape(self):
        # find product information per product url
        for url_product in self.product_page_url:
            product_page = requests.get(url_product)
            product_doc = BeautifulSoup(product_page.content, "html.parser")

            # UPC, Quantity Available, and Prices section:
            product_information_doc = product_doc.find("table", class_="table table-striped")
            #######################################################################################
            # Universal Product Code (UPC)
            self.universal_product_code.append(product_information_doc.find_all("td")[0].string)
            # Price Excluding Tax
            self.price_excluding_tax.append(product_information_doc.find_all("td")[2].string)
            # Price Including Tax
            self.price_including_tax.append(product_information_doc.find_all("td")[3].string)
            # Quantity Available
            self.quantity_available.append(product_information_doc.find_all("td")[5].string)

            # Book Title and Star rating section:
            product_information_doc1 = product_doc.find("div", class_="col-sm-6 product_main")
            ##########################################################################################
            # Book Title
            self.book_title.append(product_information_doc1.find("h1").string)
            # Review Rating
            self.review_rating.append(product_information_doc1.find("p", class_="star-rating").get("class")[1])

            # Product Description section:
            product_information_doc2 = product_doc.find("article", class_="product_page")
            #####################################################################################
            # Product Description
            self.product_description.append(product_information_doc2.find("p", class_= None).string)

            # Category Section:
            product_information_doc3 = product_doc.find("ul", class_="breadcrumb")
            ##################################################################
            # Category
            self.category.append(product_information_doc3.find("a", href="../category/books/fantasy_19/index.html").string)

            # Image Section:
            product_information_doc4 = product_doc.find("img")
            ##################################################
            # Image
            self.image_url.append(product_information_doc4.get("src").replace("../..", "https://books.toscrape.com", 1))

    def run(self):
        self.get_urls()
        self.scrape()

    def csv_file(self):
        headers = ["Book Title", "Product Page URL", "Universal Product Code (UPC)", "Price Including Tax",
                   "Price Excluding Tax", "Quantity Available", "Product Description", "Category", "Review Rating",
                   "Image URL"]
        with open("phase2.csv", "w", newline="") as file:
            # make a writer object using the file
            writer = csv.writer(file, delimiter=",")
            # create headers and columns
            writer.writerow(headers)
            for i in range(len(self.product_page_url)):
                row = [self.book_title[i], self.product_page_url[i], self.universal_product_code[i], self.price_including_tax[i], self.price_excluding_tax[i], self.quantity_available[i], self.product_description[i], self.category[i], self.review_rating[i], self.image_url[i]]
                writer.writerow(row)