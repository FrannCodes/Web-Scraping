import csv
from bs4 import BeautifulSoup
import requests

#Product Page URL

url = "https://books.toscrape.com/catalogue/category/books/fantasy_19/index.html"
end_of_page = False

product_page_url = []
universal_product_code = []
book_title = []
price_including_tax = []
price_excluding_tax = []
product_description = []
category = []
review_rating = []
image_url = []

# a loop that checks all products until the end of page
while not end_of_page:
    # declare objects and variables within loop so it can be changed
    page = requests.get(url)
    doc = BeautifulSoup(page.content, "html.parser")

    next_page = doc.find("li", class_ = "next")

    product_page_url_doc = doc.find_all("div", class_="image_container")  # gets an array elements which contains the links of the books
    for p in product_page_url_doc:
        # finds a string of elements with the tag "a"
        product = p.find("a")
        # add product page urls to an array of product_page_url:
        product_page_url.append(product.get("href").replace("../../..", "https://books.toscrape.com/catalogue", 1))

    # finding the other product information
    for url_upc in product_page_url:
        product_page = requests.get(url_upc)
        product_doc = BeautifulSoup(product_page.content, "html.parser")

        product_information_doc = product_doc.find("table", class_ = "table table-striped")
        universal_product_code = product_information_doc.find_all("tr")[0].string
        print(universal_product_code)


    if next_page is None:
        end_of_page = True
    else:
        url_section = next_page.find("a").get("href")
        url = "https://books.toscrape.com/catalogue/category/books/fantasy_19/" + url_section
print(product_page_url)



# Universal product code

#Book Title

#Price Including Tax

#Price Excluding Tax

#Quantity Available

#Product Description

#Category

#Review Rating

#Image URL

