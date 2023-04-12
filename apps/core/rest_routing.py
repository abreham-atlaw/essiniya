from rest_framework import routers

from . import viewsets

router = routers.SimpleRouter()

router.register('carts', viewsets.CartViewSet, basename='carts')

urlpatterns = router.urls