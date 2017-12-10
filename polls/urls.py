from django.conf.urls import url

from polls import views

urlpatterns = [
    url(r'^status/$', views.status, name='status'),
    url(r'^start/$', views.status, name='start'),
    url(r'^stop/$', views.status, name='stop'),
    url(r'^add/$', views.status, name='add'),
    url(r'^delete/$', views.status, name='delete'),
    url(r'^settings/$', views.status, name='settings'),
    url(r'^$', views.index, name='index')
]