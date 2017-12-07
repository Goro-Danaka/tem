from django.db import models


class ShopifySiteModel(models.Model):
    name = models.CharField(max_length=100)
    url = models.CharField(max_length=100, default='#')

    def __str__(self):
        return self.name


