from django.views.generic import View, TemplateView, ListView, FormView
from django.shortcuts import get_list_or_404, get_object_or_404



from .webcontents import StandardPage, PickupLocation
from .models import Category, Item, Cart, Order
from .forms import AddToCartForm, ContactUsForm


class StandardView(View):

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)

		context.update(StandardPage.generate_context(self.request, **kwargs))

		return context


class NewReleasesView(StandardView, TemplateView):
	template_name = 'core/new_releases_page.html'

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)

		context['items'] = Item.get_new_releases(20)

		return context


class CategoriesView(StandardView, TemplateView):
	template_name = 'core/categories_page.html'

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)

		if(self.request.GET.get('parent_category')):
			context['categories'] = get_list_or_404(
				Category, 
				parent_category__id=int(self.request.GET.get('parent_category'))
			)
			context['parent_category'] = Category.objects.get(id=int(self.request.GET.get('parent_category')))
		else:
			context['categories'] = get_list_or_404(Category, parent_category=None)
		
		return context


class ItemsView(StandardView, ListView):
	model = Item	
	template_name = 'core/category_items_page.html'
	context_object_name = 'items'
	paginate_by = 10

	def get(self, *args, **kwargs):
		self.category = get_object_or_404(Category, pk=int(kwargs.get('category')))

		return super().get(*args, **kwargs)

	def get_queryset(self, *args, **kwargs):
		return Item.objects.all().filter(category = self.category )
	
	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		print(kwargs)
		context['category'] = self.category

		return context


class ItemDetailView(StandardView, FormView):
	template_name = 'core/item_detail_page.html'
	form_class = AddToCartForm
	success_url = '/item/{}/?added=True'

	def get_form_kwargs(self, **kwargs):
		
		args = super().get_form_kwargs(**kwargs)
		
		args['item'] = get_object_or_404(Item, pk=self.kwargs.get('item'))
		if(self.request.GET.get("order")):
			args['order'] = get_object_or_404(Order, pk=self.request.GET.get("order"))
		return args

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)

		context['item'] = get_object_or_404(Item, pk=self.kwargs.get('item'))

		return context
	
	def form_valid(self, form):
		if(self.request.GET.get('order')):
			form.edit_order()
			self.success_url = '/cart/'
		else:
			form.add_to_cart(Cart.get_or_create(self.request))
			self.success_url = self.success_url.format(
				get_object_or_404(Item, pk=self.kwargs.get('item')).id
			)
		return super().form_valid(form)


class ContactUsView(StandardView, FormView):
	template_name = 'core/contact_us_page.html'
	form_class = ContactUsForm
	success_url = '/contact-us/?success=True'

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)

		context['locations'] = PickupLocation.objects.all()
		context['center_location'] = {
			'latitude': sum([location.latitude for location in context['locations']])/len(context['locations']),
			'longitude': sum([location.longitude for location in context['locations']])/len(context['locations'])
		}
		return context
	
	def form_valid(self, form):
		form.send_message()
		return super().form_valid(form)


class CartView(StandardView, TemplateView):
	template_name = 'core/cart_page.html'
	
	def get(self, request, *args, **kwargs):
		self.cart = Cart.get_or_create(self.request)
		if(request.GET.get('delete')):
			get_object_or_404(self.cart.get_orders(), id=request.GET.get('delete')).delete()
		
		return super().get(request, *args, **kwargs)


	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)

		context['cart'] = self.cart

		return context