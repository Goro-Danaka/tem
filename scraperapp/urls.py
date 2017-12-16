"""scraperhub URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from polls.api.v1.routers import api_router

urlpatterns = [
    url(r'^$', include('polls.urls')),
    url(r'^start/', include('polls.urls')),
    url(r'^stop/', include('polls.urls')),
    url(r'^add/', include('polls.urls')),
    url(r'^delete/', include('polls.urls')),
    url(r'^status/', include('polls.urls')),
    url(r'^settings/', include('polls.urls')),
    url(r'^admin/', admin.site.urls),
    url(r'api/v1/', include(api_router.urls))
]
