from rest_framework.serializers import ModelSerializer
from polls.models import ShopifySettingsModel, ShopifySiteModel, ShopifyProductModel


class ShopifySettingsSerializer(ModelSerializer):

    class Meta:
        model = ShopifySettingsModel