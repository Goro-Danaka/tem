from rest_framework import routers
from polls.api.v1.viewsets import ShopifySettingsViewSet


api_router = routers.SimpleRouter()
api_router.register('settings', ShopifySettingsViewSet)
