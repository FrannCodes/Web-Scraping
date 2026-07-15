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
quantity_available = []

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
    if next_page is None:
        end_of_page = True
    else:
        url_section = next_page.find("a").get("href")
        url = "https://books.toscrape.com/catalogue/category/books/fantasy_19/" + url_section
################################################################################################
print(product_page_url)
# find product information per product url
for url_product in product_page_url:
    product_page = requests.get(url_product)
    product_doc = BeautifulSoup(product_page.content, "html.parser")

    # UPC, Quantity Available, and Prices section:
    product_information_doc = product_doc.find("table", class_="table table-striped")
    #######################################################################################
    # Universal Product Code (UPC)
    universal_product_code.append(product_information_doc.find_all("td")[0].string)
    # Price Excluding Tax
    price_excluding_tax.append(product_information_doc.find_all("td")[2].string)
    # Price Including Tax
    price_including_tax.append(product_information_doc.find_all("td")[3].string)
    # Quantity Available
    quantity_available.append(product_information_doc.find_all("td")[5].string)

    # Book Title and Star rating section:
    product_information_doc1 = product_doc.find("div", class_ = "col-sm-6 product_main")
    ##########################################################################################
    # Book Title
    book_title.append(product_information_doc1.find("h1").string)
    # Review Rating
    review_rating.append(product_information_doc1.find("p", class_ = "star-rating").get("class")[1])

    #Product Description section:
    product_information_doc2 = product_doc.find("article", class_ = "product_page")
    #####################################################################################
    # Product Description
    product_description.append(product_information_doc2.find("p", class_ = None).string)

    #Category Section:
    product_information_doc3 = product_doc.find("ul", class_ = "breadcrumb")
    ##################################################################
    # Category
    category.append(product_information_doc3.find("a", href = "../category/books/fantasy_19/index.html").string)

    # Image Section:
    product_information_doc4 = product_doc.find("img")
    ##################################################
    # Image
    image_url.append(product_information_doc4.get("src").replace("../..", "https://books.toscrape.com", 1))



#Image URL

