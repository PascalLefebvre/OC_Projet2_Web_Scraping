from nis import cat
import requests
from bs4 import BeautifulSoup
import csv
import re

urlScrape = "http://books.toscrape.com"
# bookUrl = "http://books.toscrape.com/catalogue/vampire-knight-vol-1-vampire-knight-1_93/index.html"
categoryUrlPrefix = "http://books.toscrape.com/catalogue/category/books/sequential-art_5/"
categoryUrlSuffix = "index.html"
csvHead = ['product_pageBook_url', 'universal_product_code', 'title', 'price_including_tax',
    'price_excluding_tax', 'number_available', 'product_description', 'category',
    'review_rating', 'image_url']

# Extract the required information from the book web page
def extractBookInformation(url):
    book = [url]
    pageBook = requests.get(url)
    if pageBook.status_code == requests.codes.ok:
        soupBook = BeautifulSoup(pageBook.content, 'html.parser')
    else:
        print("Error : ", pageBook.status_code)
        exit()

    # Extract table "Product Information" (lines 2 and 5 useless)
    # line1 = UPC / line3 = HT price / line4 = TTC price
    # line6 = available stock / line7 = number of reviews
    productInformation = []
    tableLines = soupBook.find('table', class_ = "table table-striped")
    for line in tableLines.find_all('td'):
        productInformation.append(line.string)
    
    # Delete useless information
    productInformation.pop(1)
    productInformation.pop(3)
    
    # Extract the quantity of books available
    if productInformation[3].find('available') != -1:
        match = re.search(r'\d+', productInformation[3])
        if match:
            productInformation[3] = match.group()
    else:
        productInformation[3] = '0'

    # Extract title
    title = soupBook.find('h1').string.replace(',', '')

    # Extract product description 
    productPage = soupBook.find('article', class_ = 'product_page').find('p', class_ = '')
    productDescription = productPage.string.replace(',', '')

    # Extract category (last link in the concerned list)
    links = soupBook.find('ul', class_ = 'breadcrumb').find_all('a')
    for link in links:
        category = link.string

    # Extract image URL
    imageUrl = soupBook.find('div', class_ = "item active").find('img')['src'].replace('../..', '')
    imageUrl = urlScrape + imageUrl

    # "book" filled with extracted data book
    book.append(productInformation[0])
    book.append(title)
    book.append(productInformation[2])
    book.append(productInformation[1])
    book.append(productInformation[3])
    book.append(productDescription)
    book.append(category)
    book.append(productInformation[4])
    book.append(imageUrl)

    return book

# Create CSV file and write header line inside
with open("data/categories/Sequential_Art.csv", 'w') as file_csv:
    writer = csv.writer(file_csv, delimiter=',')
    writer.writerow(csvHead)
    
    # Extract books information from all the web pages of a specific category
    categoryUrl = categoryUrlPrefix + categoryUrlSuffix
    extractPage = True
    while extractPage:
        pageCategory = requests.get(categoryUrl)
        if pageCategory.status_code == requests.codes.ok:
            soupCategory = BeautifulSoup(pageCategory.content, 'html.parser')
        else:
            print("Error : ", pageCategory.status_code)
            exit()

        # Write books information from one web page in the CSV file
        booksUrl = soupCategory.find('ol', class_ = 'row').find_all('h3')
        for bk in booksUrl:
            bookUrl = urlScrape + bk.find('a')['href'].replace('../../..', '/catalogue')
            bookInformation = extractBookInformation(bookUrl)
            writer.writerow(bookInformation)
        
        # For the category, create the URL of the next web page if exists
        if soupCategory.find('li', class_ = 'next') != None:
            linkNext = soupCategory.find('li', class_ = "next").find('a')['href']
            categoryUrl = categoryUrlPrefix + linkNext
        else:
            extractPage = False
