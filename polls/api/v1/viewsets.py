from rest_framework import viewsets
from polls.models import ShopifySettingsModel, ShopifySiteModel, ShopifyProductModel
from polls.api.v1.serializers import ShopifySettingsSerializer


class ShopifySettingsViewSet(viewsets.ModelViewSet):
    queryset = ShopifySettingsModel.objects.all()
    serializer_class = ShopifySettingsSerializer