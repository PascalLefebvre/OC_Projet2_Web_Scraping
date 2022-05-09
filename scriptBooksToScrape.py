from logging import exception
from nis import cat
import requests
from bs4 import BeautifulSoup
import csv
import re

urlScrape = "http://books.toscrape.com/"
csvHeader = ['product_pageBook_url', 'universal_product_code', 'title', 'price_including_tax',
    'price_excluding_tax', 'number_available', 'product_description', 'category',
    'review_rating', 'image_url']
categoriesCsvDirectory = "./data/categories/"

# Extract the required information from the book web page
def extractBookInformation(bUrl):
    book = [bUrl]

    try:
        pageBook = requests.get(bUrl)
    except requests.exceptions.RequestException as e:
        raise SystemExit(e)
    
    soupBook = BeautifulSoup(pageBook.content, 'html.parser')

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
        matchNumber = re.search(r'\d+', productInformation[3])
        if matchNumber:
            productInformation[3] = matchNumber.group()
    else:
        productInformation[3] = '0'

    # Extract title
    title = soupBook.find('h1').string.replace(',', '')

    # Extract product description 
    productPage = soupBook.find('article', class_ = 'product_page').find('p', class_ = '')
    if productPage != None:
        productDescription = productPage.string.replace(',', '')
    else:
        productDescription = "No description"

    # Extract category (last link in the concerned list)
    links = soupBook.find('ul', class_ = 'breadcrumb').find_all('a')
    for link in links:
        category = link.string

    # Extract image URL
    imageUrl = soupBook.find('div', class_ = "item active").find('img')['src'].replace('../../', '')
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

# Extract information from all the books web pages of one category
def extractBooksCategory(cName, cUrl):
    # Create CSV books category file and write header line inside
    csvFileName = categoriesCsvDirectory + cName
    try:
        file_csv = open(csvFileName, 'w')
    except:
        print("Could not create \"", csvFileName, "\" file")
        exit()
    
    writer = csv.writer(file_csv, delimiter=',')
    writer.writerow(csvHeader)
    
    extractPage = True
    while extractPage:
        try:
            pageCategory = requests.get(cUrl)
        except requests.exceptions.RequestException as e:
            raise SystemExit(e)
        
        soupCategory = BeautifulSoup(pageCategory.content, 'html.parser')

        # Write books information from one web page in the CSV file
        booksUrl = soupCategory.find('ol', class_ = 'row').find_all('h3')
        for bk in booksUrl:
            bookUrl = urlScrape + bk.find('a')['href'].replace('../../..', 'catalogue')
            bookInformation = extractBookInformation(bookUrl)
            writer.writerow(bookInformation)
        
        # For the category, create the URL of the next web page if exists
        if soupCategory.find('li', class_ = 'next') != None:
            suffixUrl = soupCategory.find('li', class_ = "next").find('a')['href']
            prefixUrl = cUrl.rpartition('/')[0]
            cUrl = prefixUrl + '/' + suffixUrl
        else:
            extractPage = False
    
    file_csv.close()

# Create CSV file name, one per category
def createCsvFileName(ctgryUrl):
    ctgryName = ''
    categoryString = ctgryUrl.string
    matchWord = re.findall(r'\w+', categoryString)
    i = 0
    while i < len(matchWord):
        ctgryName += matchWord[i]
        i += 1
    return ctgryName

# Extract books information per category from all the "books.toscrape.com" web site 
def extractAllBooksCategories():
    try:
        pageScrape = requests.get(urlScrape)
    except requests.exceptions.RequestException as e:
        raise SystemExit(e)
    
    soupScrape = BeautifulSoup(pageScrape.content, 'html.parser')
    categoriesUrl = soupScrape.find('ul', class_ = "nav nav-list").find('ul').find_all('a')
    for catUrl in categoriesUrl:
        categoryUrl = urlScrape + catUrl['href']
        categoryName = createCsvFileName(catUrl)
        extractBooksCategory(categoryName, categoryUrl)

extractAllBooksCategories()