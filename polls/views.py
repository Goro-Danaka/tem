import os
import sys

from django.http import HttpResponse, StreamingHttpResponse
from django.shortcuts import render
from django.utils.encoding import smart_str
from wsgiref.util import FileWrapper


from polls.models import ShopifySiteModel



def index(request):
    scripts_list = ShopifySiteModel.objects.order_by('-name')[:5]
    if request.method == 'POST':
        request_paths = {
            '/status/': status,
            '/start/': start,
            '/download/': download,
            '/delete/': delete
        }
        return request_paths[request.path](request)

    context = {
        'scripts_list': scripts_list if scripts_list else None,
        'in_progress': ''
    }

    return HttpResponse(render(request, 'index.html', context))


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


def delete(request):
    #json_status = scraper.get_status()
    #response = HttpResponse(content_type='application/json')
    #response.write(json_status)
    #return response
    pass


def status(request):
    #json_status = scraper.get_status()
    #response = HttpResponse(content_type='application/json')
    #response.write(json_status)
    #return response
    pass