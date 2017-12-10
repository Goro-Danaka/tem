import json

from django.http import HttpResponse
from django.shortcuts import render

from polls.models import ShopifySiteModel
from polls.models import ShopifySettingsModel

from shopify.shopify_scraper import ShopifyScraper

_scraper = ShopifyScraper()


def index(request):
    if request.method == 'POST':
        request_paths = {
            '/status/': status,
            '/start/': start,
            '/stop/': stop,
            '/add/': add,
            '/delete/': delete
        }
        return request_paths[request.path](request)

    websites_list = ShopifySiteModel.objects.order_by('-name')
    settings = ShopifySettingsModel.objects.order_by('-name')[:1]

    context = {
        'website_list': websites_list,
        'settings': settings
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
            is_shopify_site = _scraper.is_shopify_site(website_url)
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


def start(request):
    websites_list = ShopifySiteModel.objects.order_by('-name')
    result = {}
    response = HttpResponse(content_type='application/json')
    try:
        for website in websites_list:
            _scraper.start(website.url)
        result['success'] = True
    except Exception as ex:
        result['success'] = False
        result['message'] = 'Exception was thrown: "%s"' % ex
    finally:
        json_result = json.dumps(result)
        response.write(json_result)
        return response


def stop(request):
    response = HttpResponse(content_type='application/json')
    _scraper.stop()
    return response


def status(request):
    json_status = json.dumps(_scraper.get_status())
    response = HttpResponse(content_type='application/json')
    response.write(json_status)
    return response

