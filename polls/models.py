from django.db import models
from polls.result_enum import status
from datetime import datetime


class ShopifySiteModel(models.Model):
    name = models.CharField(max_length=100)
    url = models.CharField(max_length=100, default='http://example.com')
    total_products = models.IntegerField(default=0)
    last_update_date = models.DateTimeField(default=datetime.now())
    last_status = models.CharField(max_length=100, default=status[0])

    def __str__(self):
        return self.name


class ShopifySettingsModel(models.Model):
    name = models.CharField(max_length=100)
    proxy_api = models.CharField(max_length=100, default='')
    update_period = models.IntegerField(default=60)

    def __str__(self):
        return self.name


class ShopifyProductModel(models.Model):
    website_id = models.IntegerField(default=0)
    title = models.CharField(max_length=200, default='')
    category = models.CharField(max_length=200, default='')
    url = models.CharField(max_length=200, default='')
    description = models.CharField(max_length=200, default='')
    price = models.CharField(max_length=200, default='')
    sale_price = models.CharField(max_length=200, default='')
    currency = models.CharField(max_length=200, default='')
    images = models.CharField(max_length=2000, default='')

    def __str__(self):
        return self.title


