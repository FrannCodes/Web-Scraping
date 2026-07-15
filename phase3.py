import csv
from bs4 import BeautifulSoup
import requests

url = "https://books.toscrape.com/index.html"
category_url = []# a list that will contain all category urls
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
categories = {}

page = requests.get(url)
doc = BeautifulSoup(page.content, "html.parser")

category_url_doc = doc.find("ul", class_ = "nav nav-list")
category_url_doc1 = category_url_doc.find_all("li")
category_url_doc1.pop(0) # removes the "Books" category link
for c in category_url_doc1:
    category_doc2 = c.find("a")
    category_url.append("https://books.toscrape.com/" + category_doc2.get("href"))
    categories [category_doc2.string] = []

for c in category_url:
    end_of_page = False
    while not end_of_page:
        # declare objects and variables within loop so it can be changed
        page1 = requests.get(c)
        doc1 = BeautifulSoup(page1.content, "html.parser")

        next_page = doc1.find("li", class_="next")

        product_page_url_doc = doc1.find_all("div", class_="image_container")  # gets a list of elements which contains the links of the books
        for p in product_page_url_doc:
            # finds a string of elements with the tag "a"
            product = p.find("a")
            # add product page urls to an array of product_page_url:
            product_page_url.append(product.get("href").replace("../../..", "https://books.toscrape.com/catalogue", 1))

            # Category Section:
            category_doc = doc1.find("li", class_ = "active")
            # append category to category list per each product url visited
            category.append(category_doc.string)



        if next_page is None:
            end_of_page = True
        else:
            category_url_section = c.rsplit("/", 1)[0] + "/"
            url_section = next_page.find("a").get("href")
            c = category_url_section + url_section

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
    product_information_doc1 = product_doc.find("div", class_="col-sm-6 product_main")
    ##########################################################################################
    # Book Title
    book_title.append(product_information_doc1.find("h1").string)
    # Review Rating
    review_rating.append(product_information_doc1.find("p", class_="star-rating").get("class")[1])

    # Product Description section:
    product_information_doc2 = product_doc.find("article", class_="product_page")
    #####################################################################################
    # Product Description
    description = product_information_doc2.find("p", class_= None)
    if description is not None:
        product_description.append(description.string)
    else:
         product_description.append("No description")

    # Image Section:
    product_information_doc4 = product_doc.find("img")
    ##################################################
    # Image
    image_url.append(product_information_doc4.get("src").replace("../..", "https://books.toscrape.com", 1))

headers = ["Book Title", "Product Page URL", "Universal Product Code (UPC)", "Price Including Tax", "Price Excluding Tax", "Quantity Available", "Product Description", "Category", "Review Rating", "Image URL"]
for a in category:
    with open(a + ".csv", "w", newline="") as file:
        # make a writer object using the file
        writer = csv.writer(file, delimiter=",")
        # create headers and columns
        writer.writerow(headers)
        for i in range(len(product_page_url)):
            row = [book_title[i], product_page_url[i], universal_product_code[i], price_including_tax[i],
                   price_excluding_tax[i], quantity_available[i], product_description[i], category[i], review_rating[i],
                   image_url[i]]
            writer.writerow(row)
