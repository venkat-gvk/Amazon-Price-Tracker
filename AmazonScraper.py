from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
import time


def init():
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    options.add_experimental_option("excludeSwitches", ["enable-logging"])
    return webdriver.Chrome('./chromedriver', options=options)


class AmazonScraper:
    def __init__(self, url, search_name):
        self.driver = init()
        self.url = url
        self.search_name = search_name

    def getProductTitle(self):
        try:
            productTitle = self.driver.find_element_by_id('productTitle')
            return productTitle.text

        except:
            Exception()
            return None

    def getProductPrice(self, product_ID):
        try:
            productPrice = self.driver.find_element_by_id(
                'priceblock_ourprice')
            price = productPrice.text

            def convertPrice():
                nonlocal price    
                res = price.split('₹')
                if len(res) > 1:
                    price = res[1].split(',')

                price = float(''.join(price))

            convertPrice()

            return price

        except NoSuchElementException:
            print(f"Can't find price for the product with ID: {product_ID}")
            print("Skipping this product")
            return None

    def getProductSeller(self, product_ID):
        try:
            productSeller = self.driver.find_element_by_id(
                'sellerProfileTriggerId')
            return productSeller.text

        except NoSuchElementException:
            print(f"Can't find seller for the product with ID: {product_ID}")
            return None

    def sortByPrice(self, products):
        return sorted(products, key=lambda product: product['price'])

    def getIndividualProducts(self, links):
        print(f"Found {len(links)} links")
        print('Getting Product_ID and Price for each products...')

        products = []

        for link in links:
            t = link.split('/dp/')
            product_ID = None

            if len(t) > 1:
                product_ID = t[1]
            else:
                product_ID = t[0]

            self.driver.get(link)

            print('Getting price for the ID:', product_ID)

            productTitle = self.getProductTitle()
            productPrice = self.getProductPrice(product_ID)
            productSeller = self.getProductSeller(product_ID)

            if productTitle and productPrice and productSeller:
                obj = {
                    'title': productTitle,
                    'url': link,
                    'ID': product_ID,
                    'price': productPrice,
                    'seller': productSeller
                }
                products.append(obj)

        return self.sortByPrice(products)

    def urlCleanUp(self, links):
        cleanedURL = []

        for link in links:
            redirect = link.find('Redirect.html')
            slredirect = link.find('slredirect')

            if redirect != -1 or slredirect != -1:
                modifiedURL = self.url + '/'
                res = link.split('&url=%2F')[1].split('%2', 1)[0]
                product_id = link.split('dp%2F')[1].split('%2F')[0]
                modifiedURL = modifiedURL + res + '/dp/' + product_id
                cleanedURL.append(modifiedURL)

            else:
                endIndex = link.find('/ref')
                cleanedURL.append(link[0:endIndex])

        return cleanedURL

    def getLinksforTheProduct(self):
        links = []
        results = self.driver.find_elements_by_xpath('//*[@id="search"]/div[1]/div[1]/div/span[3]/div[2]/*/div//div[2]/div/div/div[1]/h2/a');
        time.sleep(3)

        try:
            for result in results:
                link = result.get_attribute('href')
                links.append(link)

        except Exception:
            print("Can't get any links for", self.search_name)

        return links

    # initiate scraper    

    def run(self):
        print('Starting Amazon Scraper')
        time.sleep(2)

        print('Initializing...')
        print('Searching for', self.search_name, '...')

        self.driver.implicitly_wait(15)
        self.driver.get(self.url)
        inputElement = self.driver.find_element_by_id('twotabsearchtextbox')

        if not inputElement:
            print("Search term not found")
            print('scrapping stops...')
            self.quitScarper()

        inputElement.clear()
        inputElement.send_keys(self.search_name)
        inputElement.send_keys(Keys.RETURN)
        links = self.getLinksforTheProduct()

        if not links:
            print('No search links available for the product',
                  self.search_name)
            self.quitScraper()
            return

        links = self.urlCleanUp(links)
        products = self.getIndividualProducts(links)

        self.quitScraper()

        return products

    def quitScraper(self):
        print('Stopping...')
        self.driver.quit()
