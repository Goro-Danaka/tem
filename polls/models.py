from django.db import models
from django.utils.encoding import smart_str

from polls.result_enum import status
from datetime import datetime


class ShopifySiteModel(models.Model):
    name = models.CharField(max_length=100, verbose_name='Name')
    url = models.CharField(max_length=100, default='http://example.com', verbose_name='Url')
    total_products = models.IntegerField(default=0, verbose_name='Total products')
    last_update_date = models.DateTimeField(default=datetime.now(), verbose_name='Last update date')
    last_status = models.CharField(max_length=100, default=status[0], verbose_name='Last update status')

    def __str__(self):
        return smart_str('%s (%s)' % (self.name, self.url))

    def __unicode__(self):
        return u'%s (%s)' % (self.name, self.url)


class ShopifySettingsModel(models.Model):
    name = models.CharField(max_length=100, verbose_name='Name')
    proxy_api = models.CharField(max_length=100, default='', verbose_name='Proxy api key')
    update_period = models.IntegerField(default=60, verbose_name='Update after (sec)')

    def __str__(self):
        return smart_str(self.name)

    def __unicode__(self):
        return self.name


class ShopifyProductModel(models.Model):
    website = models.ForeignKey(ShopifySiteModel, null=True, verbose_name='Parent website')
    title = models.CharField(max_length=200, default='', verbose_name='Title')
    category = models.CharField(max_length=200, default='', verbose_name='Category name')
    url = models.CharField(max_length=200, default='', verbose_name='Url')
    description = models.CharField(max_length=200, default='', verbose_name='Short description')
    price = models.CharField(max_length=200, default='', verbose_name='Price')
    sale_price = models.CharField(max_length=200, default='', verbose_name='Sale price')
    currency = models.CharField(max_length=200, default='', verbose_name='Currency')
    images = models.CharField(max_length=2000, default='', verbose_name='Images urls')

    def __str__(self):
        return smart_str('%s' % self.title)

    def __unicode__(self):
        return '%s' % self.title



