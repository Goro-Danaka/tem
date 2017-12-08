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


