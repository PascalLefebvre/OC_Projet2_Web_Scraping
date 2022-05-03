import requests
from bs4 import BeautifulSoup
import csv
import re

urlScrape = "http://books.toscrape.com"
productPageUrl = "http://books.toscrape.com/catalogue/vampire-knight-vol-1-vampire-knight-1_93/index.html"
csvHead = ['product_page_url', 'universal_product_code', 'title', 'price_including_tax',
    'price_excluding_tax', 'number_available', 'product_description', 'category',
    'review_rating', 'image_url']

bookInformation = [productPageUrl]

page = requests.get(productPageUrl)

if page.status_code == requests.codes.ok:
    soup = BeautifulSoup(page.content, 'html.parser')
else:
    print("Error : ", page.status_code)
    exit()

# Extract table "Product Information" (lines 2 and 5 useless)
# line1 = UPC / line3 = HT price / line4 = TTC price
# line6 = available stock / line7 = number of reviews
productInformation = []
tableLines = soup.find('table', class_ = "table table-striped")
for line in tableLines.find_all('td'):
    productInformation.append(line.string)
productInformation.pop(1)
productInformation.pop(3)
if productInformation[3].find('available') != -1:
    match = re.search(r'\d+', productInformation[3])
    if match:
        productInformation[3] = match.group()
else:
    productInformation[3] = '0'

# Extract title
title = soup.find('h1').string.replace(',', '')

# Extract product description 
productPage = soup.find('article', class_ = 'product_page').find('p', class_ = '')
productDescription = productPage.string.replace(',', '')

# Extract category (last link in the list)
links = soup.find('ul', class_ = 'breadcrumb').find_all('a')
for link in links:
    category = link.string

# Extract image URL
imageUrl = soup.find('div', class_ = "item active").find('img')['src'].replace('../..', '')
imageUrl = urlScrape + imageUrl

# bookInformation filled with extracted data book
bookInformation.append(productInformation[0])
bookInformation.append(title)
bookInformation.append(productInformation[2])
bookInformation.append(productInformation[1])
bookInformation.append(productInformation[3])
bookInformation.append(productDescription)
bookInformation.append(category)
bookInformation.append(productInformation[4])
bookInformation.append(imageUrl)

# Create CSV file and save book information inside
with open("data/bookInformation.csv", 'w') as file_csv:
    writer = csv.writer(file_csv, delimiter=',')
    writer.writerow(csvHead)
    writer.writerow(bookInformation)