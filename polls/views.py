import os
import sys
import json

from django.http import HttpResponse, StreamingHttpResponse
from django.shortcuts import render
from django.utils.encoding import smart_str
from wsgiref.util import FileWrapper


from polls.models import ShopifySiteModel


def index(request):
    if request.method == 'POST':
        request_paths = {
            '/status/': status,
            '/start/': start,
            '/add/': add,
            '/delete/': delete
        }
        return request_paths[request.path](request)

    websites_list = ShopifySiteModel.objects.order_by('-name')

    context = {
        'website_list': websites_list if websites_list else None,
        'in_progress': ''
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
            new_website = ShopifySiteModel(name=website_name, url=website_url)
            new_website.save()
            result['success'] = True
        else:
            result['success'] = False
    except Exception as ex:
        result['success'] = False
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


def start(request):
    #selected_script = request.POST['selected_script']
    #scraper.select_script(selected_script)
    #scraper.start()
    #response = HttpResponse(content_type='application/json')
    #return response
    pass


def download(request):
    #file_name = request.POST['file_name']
    #result_path = os.path.join(sys.path[0], 'results')
    #result_file_path = os.path.join(result_path, file_name)
    #is_file_exist = os.path.isfile(result_file_path)
    #chunk_size = 16384
    #if os.path.exists(result_file_path) and is_file_exist:
    #    response = StreamingHttpResponse(FileWrapper(open(result_file_path, 'rb'), chunk_size),
    #                                     content_type='text/csv')
    #    response['Content-Disposition'] = 'attachment; filename="%s"' % file_name
    #    response['Content-Length'] = os.path.getsize(result_file_path)
    #    return response
    pass

def status(request):
    #json_status = scraper.get_status()
    #response = HttpResponse(content_type='application/json')
    #response.write(json_status)
    #return response
    pass
