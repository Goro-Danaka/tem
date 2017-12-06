from providers.browsers.request_browser import Browser
from shopify.shopify_scraper import ShopifyScraper

if __name__ == '__main__':
    browser = Browser()
    app = ShopifyScraper(browser=browser)
