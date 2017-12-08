from django.contrib import admin
from polls.models import ShopifySiteModel
from polls.models import ShopifySettingsModel

admin.site.register(ShopifySiteModel)
admin.site.register(ShopifySettingsModel)
