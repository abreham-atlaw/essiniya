from django.views.generic import TemplateView, View
from django.core.exceptions import PermissionDenied

from apps.core.webcontents import Tab
from apps.core.models import Cart

class AdminView(View):
	def get(self, *args, **kwargs):
		if(not self.request.user.is_superuser):
			raise PermissionDenied
		return super().get(*args, **kwargs)

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)

		context['tabs'] = Tab.objects.filter(to="admin_site").order_by("order")

		return context

class OrdersView(AdminView, TemplateView):
	template_name = 'admin_site/orders_page.html'

	