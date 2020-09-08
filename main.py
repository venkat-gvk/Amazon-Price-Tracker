import sys
from AmazonScraper import AmazonScraper
from GenerateReport import GenerateReport

SEARCH_NAME = ''
URL = 'https://www.amazon.in'


def getSearchName():
    global SEARCH_NAME
    SEARCH_NAME = input('Enter search term: ')
    SEARCH_NAME = SEARCH_NAME.strip()

    if SEARCH_NAME == '':
        print('Invalid input')
        sys.exit()


if __name__ == '__main__':
    getSearchName()
    amazon = AmazonScraper(URL, SEARCH_NAME)
    products = amazon.run()

    if not products:
        sys.exit()

    GenerateReport(SEARCH_NAME, URL, products)
