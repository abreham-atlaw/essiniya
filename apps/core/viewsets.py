from django.core.exceptions import PermissionDenied

from rest_framework.viewsets import ViewSet, ReadOnlyModelViewSet

from .serializers import CartSerializer
from .models import Cart
class AdminViewSet(ViewSet):

	def check_permissions(self, request):
		if(not request.user.is_superuser):
			raise PermissionDenied
	
		return super().check_permissions(request)


class CartViewSet(AdminViewSet, ReadOnlyModelViewSet):

	serializer_class = CartSerializer
	
	def get_queryset(self):
		if(self.request.GET.get('new')):
			return Cart.objects.all().filter(ordered=True, done=False)
		return Cart.objects.all().filter(ordered=True)
	