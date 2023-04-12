from django.urls import path
from django.views.generic import RedirectView
from . import views
from . import webcontents


def register_page_urls():
	global urlpatterns

	urlpatterns += [
		path('about-us/', RedirectView.as_view(url=webcontents.AboutUsPage.objects.all()[0].url)),
		path('', RedirectView.as_view(url=webcontents.HomePage.objects.all()[0].url))
	]

urlpatterns = [
	path('new-releases/', views.NewReleasesView.as_view()),
	path('categories/', views.CategoriesView.as_view()),
	path('category/<int:category>/items/', views.ItemsView.as_view()),
	path('item/<int:item>/', views.ItemDetailView.as_view()),
	path('cart/', views.CartView.as_view()),
	path('contact-us/', views.ContactUsView.as_view()),

]

try:
	#register_page_urls()
	pass
except IndexError:
	print('[-]Some REDIRECT URLS were not added due to Page instance not being created.')

