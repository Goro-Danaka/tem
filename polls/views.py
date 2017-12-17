import json
import time

from django.http import HttpResponse
from django.shortcuts import render

from polls.models import ShopifyProductModel
from polls.models import ShopifySettingsModel
from polls.models import ShopifySiteModel

from providers.logging_provider import LoggingProvider
from providers.google_sheets import GoogleSheets
from shopify.shopify_scraper import ShopifyScraper
from datetime import datetime


scraper_settings = ShopifySettingsModel.objects.order_by('-name')
scraper = ShopifyScraper(scraper_settings[0])
google_sheets = GoogleSheets()
lp = LoggingProvider()
in_progress = False


def index(request):
    if request.method == 'POST':
        request_paths = {
            '/status/': status,
            '/start/': start,
            '/stop/': stop,
            '/add/': add,
            '/settings/': settings,
            '/delete/': delete
        }
        return request_paths[request.path](request)

    websites_list = ShopifySiteModel.objects.order_by('-name')
    settings_list = ShopifySettingsModel.objects.order_by('-name')

    context = {
        'website_list': websites_list,
        'settings_list': settings_list
    }

    return HttpResponse(render(request, 'index.html', context))


def add(request):
    websites_list = ShopifySiteModel.objects.order_by('-name')
    result = {}
    response = HttpResponse(content_type='application/json')
    try:
        website_name = request.POST['website_name']
        website_url = request.POST['website_url']
        is_exist = False
        for website in websites_list:
            if website.name.lower() == website_name.lower()\
                    or website.url.lower() == website_url.lower():
                is_exist = True
                break
        if not is_exist:
            is_shopify_site = scraper.is_shopify_site(website_url)
            if is_shopify_site:
                new_website = ShopifySiteModel(name=website_name, url=website_url)
                new_website.save()
                result['success'] = True
            else:
                result['success'] = False
                result['message'] = 'Website isn\'t SHOPIFY!'
        else:
            result['success'] = False
            result['message'] = 'Website with this URL or name already exist!'
    except Exception as ex:
        result['success'] = False
        result['message'] = 'Exception was thrown: "%s"' % ex
    finally:
        json_result = json.dumps(result)
        response.write(json_result)
        return response


def delete(request):
    response = HttpResponse(content_type='application/json')
    result = {}
    try:
        ids_to_delete = request.POST.getlist('ids_to_delete[]')
        for id_to_delete in ids_to_delete:
            website = ShopifySiteModel.objects.get(id=id_to_delete)
            website.delete()
        result['success'] = True
    except Exception as ex:
        result['success'] = False
    finally:
        json_result = json.dumps(result)
        response.write(json_result)
        return response


def settings(request):
    response = HttpResponse(content_type='application/json')
    result = {}
    try:
        settings_list = ShopifySettingsModel.objects.order_by('-name')
        proxy_api_key = request.POST['proxy_api_key']
        update_period = request.POST['update_period']
        for settings_entry in settings_list:
            settings_entry.proxy_api = proxy_api_key
            settings_entry.update_period = int(update_period)
            settings_entry.save()
            scraper.set_settings(settings_entry)
        result['success'] = True
    except Exception as ex:
        result['success'] = False
        result['message'] = 'Exception was thrown: "%s"' % ex
    finally:
        json_result = json.dumps(result)
        response.write(json_result)
        return response


def start(request):
    global in_progress
    result = {}
    response = HttpResponse(content_type='application/json')
    try:
        in_progress = True
        scraper_products()
        result['success'] = True
    except Exception as ex:
        result['success'] = False
        result['message'] = 'Exception was thrown: "%s"' % ex
    finally:
        json_result = json.dumps(result)
        response.write(json_result)
        in_progress = False
        return response


def stop(request):
    global in_progress
    response = HttpResponse(content_type='application/json')
    scraper.stop()
    in_progress = False
    return response


def status(request):
    global in_progress
    scraper_status = scraper.get_status()
    scraper_status['in_progress'] = in_progress
    json_status = json.dumps(scraper_status)
    response = HttpResponse(content_type='application/json')
    response.write(json_status)
    return response


def create_entries(all_products_info, website_id, website_name):
    try:
        google_sheets.set_worksheet(website_name)
        for product_info in all_products_info:
            products = ShopifyProductModel.objects.filter(url=product_info['Url'])
            products_count = products.count()
            #google_sheets.update(product_info)
            if products_count:
                continue
            entry = ShopifyProductModel(
                website=ShopifySiteModel.objects.filter(id=website_id)[0],
                title=product_info['Title'] if product_info['Title'] else '',
                category=product_info['Category'] if product_info['Category'] else '',
                url=product_info['Url'] if product_info['Url'] else '',
                description=product_info['Description'] if product_info['Description'] else '',
                price=product_info['Price'] if product_info['Price'] else '',
                sale_price=product_info['Sale price'] if product_info['Sale price'] else '',
                currency=product_info['Currency'] if product_info['Currency'] else '',
                images=get_images_string(product_info['Images']))
            entry.save()
    except Exception as ex:
        lp.warning('Some problem while creating entry. Exception: "%s"' % ex)


def update_website_info(website_id, scraper_status):
    try:
        website = ShopifySiteModel.objects.get(id=website_id)
        website.total_products = scraper_status['total_products']
        website.last_update_date = datetime.now()
        website.last_status = 'Success' if scraper_status['success'] else 'Failed'
        website.save()
    except Exception as ex:
        pass


def get_images_string(images):
    result = ''
    for image in images:
        result += '%s;' % image
    return result


def scraper_products():
    global in_progress

    while True:
        if not in_progress:
            return
        websites_list = ShopifySiteModel.objects.order_by('-name')
        settings_list = ShopifySettingsModel.objects.order_by('-name')

        update_period = 0

        for settings_item in settings_list:
            update_period = settings_item.update_period

        for website in websites_list:
            if in_progress:
                all_products_info = scraper.scrape(website.url)
                scraper_status = scraper.get_status()
                create_entries(all_products_info, website_id=website.id, website_name=website.name)
                update_website_info(website_id=website.id, scraper_status=scraper_status)
        time.sleep(update_period)


