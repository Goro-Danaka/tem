from django.contrib import admin
from polls.models import ShopifySiteModel
from polls.models import ShopifySettingsModel
from polls.models import ShopifyProductModel

admin.site.register(ShopifySiteModel)
admin.site.register(ShopifySettingsModel)
admin.site.register(ShopifyProductModel)