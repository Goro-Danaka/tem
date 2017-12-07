from django.conf.urls import url

from polls import views

urlpatterns = [
    url(r'^status/$', views.status, name='status'),
    url(r'^start/$', views.status, name='start'),
    url(r'^download/$', views.status, name='download'),
    url(r'^delete/$', views.status, name='delete'),
    url(r'^$', views.index, name='index')
]