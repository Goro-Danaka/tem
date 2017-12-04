from providers.browsers.request_browser import Browser
from shopify.product_fields import ProductFields

if __name__ == '__main__':
    product_url = 'https://silobeauty.com/collections/face/products/24k-gold-beauty-bar-pulse-facial-roller'
    browser = Browser()
    app = ProductFields(browser).get_product_fields(product_url)
