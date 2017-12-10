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
    MINUTE = 'minute'
    HOUR = 'hour'
    DAY = 'day'

    UPDATE_PERIOD_CHOICES = (
        (MINUTE, 'Minute'),
        (HOUR, 'Hour'),
        (DAY, 'Day')
    )

    update_period_dict = {
        MINUTE: 60,
        HOUR: 3600,
        DAY: 86400
    }

    name = models.CharField(max_length=100)
    proxy_api = models.CharField(max_length=100, default='')
    update_period = models.CharField(max_length=6,
                                     choices=UPDATE_PERIOD_CHOICES,
                                     default=MINUTE)

    def __str__(self):
        return self.name

    def update_period_seconds(self):
        return self.update_period_dict[self.update_period]


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


