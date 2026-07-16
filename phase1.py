import csv
from bs4 import BeautifulSoup
import requests

url = "https://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html"

class Scraper:
    def __init__(self, url):
        self.url = url

page = requests.get(url)
doc = BeautifulSoup(page.content, "html.parser")

#Product Page URL
product_page_url = page.url

# Universal product code
universal_product_code_doc = doc.find_all("tr")[0]
universal_product_code = universal_product_code_doc.find("td").string
print(universal_product_code)

#Book Title
book_title = doc.title.string
print(book_title)

#Price Including Tax
price_including_tax_doc = doc.find_all("tr")[3]
price_including_tax = price_including_tax_doc.find("td").string
print(price_including_tax)

#Price Excluding Tax
price_excluding_tax_doc = doc.find_all("tr")[2]
price_excluding_tax = price_excluding_tax_doc.find("td").string
print(price_excluding_tax)

#Quantity Available
quantity_available_doc = doc.find_all("tr")[5]
quantity_available = quantity_available_doc.find("td").string
print(quantity_available)

#Product Description
product_description_doc = doc.find("article", class_="product_page")
product_description = product_description_doc.find_all("p")[-1].string
print(product_description)

#Category
category_doc = doc.find_all("li")[2]
category = category_doc.find("a").string
print(category)

#Review Rating
review_rating_doc = doc.find("p", class_ = "star-rating")
review_rating = review_rating_doc.get("class")[1]
print(f"{review_rating} out of Five Stars")

#Image URL
image_url_doc = doc.find("img")
image_url_text = image_url_doc.get("src")
image_url = image_url_text.replace("../..", "https://books.toscrape.com", 1)
print(image_url)

#CSV file
headers = ["Book Title", "Product Page URL", "Universal Product Code (UPC)", "Price Including Tax", "Price Excluding Tax", "Quantity Available", "Product Description", "Category", "Review Rating", "Image URL"]
columns = [book_title, product_page_url, universal_product_code, price_including_tax, price_excluding_tax, quantity_available, product_description, category, review_rating, image_url]
with open("phase1.csv", "w", newline = "") as file:
    #make a writer object using the file
    writer = csv.writer(file, delimiter = ",")
    #create headers and columns
    writer.writerow(headers)
    writer.writerow(columns)
