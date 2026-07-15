import csv
from bs4 import BeautifulSoup
import requests

url = "https://books.toscrape.com/index.html"
category_url = {}# a dictionary that will contain all category urls
product_page_url = {}
universal_product_code = {}
book_title = {}
price_including_tax = {}
price_excluding_tax = {}
product_description = {}
category = {}
review_rating = {}
image_url = {}
quantity_available = {}
categories = {}

page = requests.get(url)
doc = BeautifulSoup(page.content, "html.parser")

category_url_doc = doc.find("ul", class_ = "nav nav-list")
category_url_doc1 = category_url_doc.find_all("li") #
category_url_doc1.pop(0) # removes the "Books" category link
for c in category_url_doc1:
    category_doc2 = c.find("a")
    categories [category_doc2.string] = []

for url_product in product_page_url:
    product_page = requests.get(url_product)
    product_doc = BeautifulSoup(product_page.content, "html.parser")

    product = {
        "Book Title" : [],
        "Product Page URL" : [],
        "Universal Product Code (UPC)" : [],
        "Price Including Tax" : [],
        "Price Excluding Tax" : [],
        "Quantity Available" : [],
        "Product Description" : [],
        "Category" : [],
        "Review Rating" : [],
        "Image URL" : []
    }