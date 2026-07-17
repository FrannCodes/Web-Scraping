import csv
from bs4 import BeautifulSoup
import requests

class Scraper:
    def __init__(self, url):
        self.url = url
        self.categories = {}

    def scrape(self):
        page = requests.get(self.url)
        doc = BeautifulSoup(page.content, "html.parser")

        category_url_doc = doc.find("ul", class_="nav nav-list")
        category_url_doc1 = category_url_doc.find_all("li")  #
        category_url_doc1.pop(0)  # removes the "Books" category link

        for c in category_url_doc1:

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

            # category url
            category_url = "https://books.toscrape.com/" + c.find("a").get("href")
            # finding the end of page per category
            end_of_page = False
            # change the category url as it checks for next page
            while not end_of_page:
                page1 = requests.get(category_url)
                doc1 = BeautifulSoup(page1.content, "html.parser")
                product_page_url_doc = doc1.find_all("div",
                                                     class_="image_container")  # gets a list of elements which contains the links of the books
                for p in product_page_url_doc:
                    # finds a string of elements with the tag "a"
                    product = p.find("a")
                    # add product page urls to an array of product_page_url:
                    product_page_url.append(
                        product.get("href").replace("../../..", "https://books.toscrape.com/catalogue", 1))
                    # Category Section:
                    category_doc = doc1.find("li", class_="active")
                    # append category to category list per each product url
                    category.append(category_doc.string)

                # finds the section of the url for the next page
                next_page = doc1.find("li", class_="next")
                if next_page is None:
                    end_of_page = True
                else:
                    category_url_section = category_url.rsplit("/", 1)[0] + "/"
                    url_section = next_page.find("a").get("href")
                    category_url = category_url_section + url_section

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

            # adds a list value per key; a list of ordered product information per header
            products = {
                "Book Title": book_title,
                "Product Page URL": product_page_url,
                "Universal Product Code (UPC)": universal_product_code,
                "Price Including Tax": price_including_tax,
                "Price Excluding Tax": price_excluding_tax,
                "Quantity Available": quantity_available,
                "Product Description": product_description,
                "Category": category,
                "Review Rating": review_rating,
                "Image URL": image_url
            }
            self.categories[c.find("a").string.strip()] = products

    def csv_file(self):
        # opens files based on categories
        for key, value in self.categories.items():
            # opens file with the file name as category name
            headers = value.keys()
            with open(key + ".csv", "w", newline="") as file:
                writer = csv.writer(file, delimiter=",")
                writer.writerow(headers)

                number_of_books = len(value["Book Title"])

                for i in range(number_of_books):
                    row = []
                    for v in value.values():
                        row.append(v[i])
                    writer.writerow(row)