from providers.request_browser import Browser
from providers.database_provider import DatabaseProvider
from shopify.shopify_scraper import ShopifyScraper

if __name__ == '__main__':
    browser = Browser()
    database_provider = DatabaseProvider()
    app = ShopifyScraper(browser=browser)
