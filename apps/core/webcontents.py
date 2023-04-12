from django.db import models

from wagtail.core.models import Page
from wagtail.core.blocks import StructBlock, CharBlock, RichTextBlock, StreamBlock
from wagtail.core.fields import RichTextField, StreamField
from wagtail.core.blocks import CharBlock, URLBlock, TextBlock
from wagtail.admin.edit_handlers import FieldPanel, RichTextFieldPanel, MultiFieldPanel, StreamFieldPanel
from wagtail.images.blocks import ImageChooserBlock
from wagtail.documents.blocks import DocumentChooserBlock

import random


class Tab(models.Model):
	name = models.CharField(max_length=50)
	url = models.CharField(max_length=100, blank=True, null=True)
	to = models.CharField(max_length=10, choices=[
		('header', "Header"),
		('footer', "Footer"),
		('admin_site', "Admin Site")
	])
	order = models.IntegerField(default=0)
	fa_icon = models.CharField(max_length=50, null=True, blank=True)

	def __str__(self):
		return '{} - {}'.format(self.name, self.to)


class ContactInformation(models.Model):
	key = models.CharField(max_length=100)
	link= models.CharField(max_length=100, null=True, blank=True)
	value = models.CharField(max_length=100)
	

class SocialMedia(models.Model):
	name = models.CharField(max_length=100)
	image = models.ImageField(upload_to="core/webcontents/socialmedia/")
	url = models.CharField(max_length=200)


class PickupLocation(models.Model):
	longitude = models.DecimalField(max_digits=10, decimal_places=8)
	latitude = models.DecimalField(max_digits=10, decimal_places=8)
	description = models.CharField(max_length=100)

	def __str__(self):
		return self.description


class PageFolder(Page):
	url = '/'

	def get_allowed_subpage_models(self):
		if(self.title in ALLOWED_SUBPAGES):
			return ALLOWED_SUBPAGES[self.title]
		return None

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		PageFolder._clean_subpage_models = self.get_allowed_subpage_models()


class StandardPage(Page):
	
	def get_context(self, request, *args, **kwargs):
		context = super().get_context(request, *args, **kwargs)

		context.update(StandardPage.generate_context(request, **kwargs))

		return context
	
	@staticmethod
	def generate_context(request, **kwargs):
		from .models import Cart
		context = {}

		context['header_tabs'] = Tab.objects.filter(to='header').order_by('order')
		context['footer_tabs'] = Tab.objects.filter(to='footer').order_by('order')
		context['contact_informations'] = ContactInformation.objects.all()
		context['social_media'] = SocialMedia.objects.all()

		context['cart_items_length'] = len(Cart.get_or_create(request).get_orders())

		return context


class MenuPage(StandardPage):
	page_title = ''
	page_slug = ''

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		if(self.page_title):
			self.title = self.page_title
			if not self.page_slug:
				self.slug = self.title.lower()
			if self.page_slug:
				self.slug = self.page_slug


class ImageBlock(StructBlock):
	image = ImageChooserBlock(required=True)
	alt = CharBlock(required=False)
	description = RichTextBlock(required=False, help_text="Description to be displayed under the image.")

	class Meta:
		icon='image'
		template = 'core/webcontents/image_template.html'


class VideoBlock(StructBlock):
	video = DocumentChooserBlock(required=True, help_text='upload_video')
	description = RichTextBlock(required=False, help_text="Description to be displayed under the video")

	class Meta:
		icon = 'media'
		template = 'core/webcontents/video_template.html'


class QuoteBlock(StructBlock):
	text = RichTextBlock(required=True, null=False, blank=False)
	source = CharBlock(required=False, null=True, blank=True)

	class Meta:
		icon='openquote'
		template = 'core/webcontents/quote_template.html'


class FlexibleContent(StreamBlock):
	image = ImageBlock(required=False)
	text = RichTextBlock(required=True, null=False, blank=False)
	quote = QuoteBlock(required=False)
	video = VideoBlock(required=False)

	class Meta:
		template = 'core/webcontents/flexible_content_template.html'


class AboutUsPage(MenuPage):
	
	background = models.ImageField(upload_to="core/about_us/")
	
	who_we_are_image = models.ImageField(upload_to="core/about_us/")
	who_we_are_text = RichTextField()

	services_image = models.ImageField(upload_to="core/about_us/")
	services_text = RichTextField()

	content_panels =  [
		FieldPanel('background'),

		MultiFieldPanel([
			FieldPanel('who_we_are_image'),
			FieldPanel('who_we_are_text')
		], heading="Who We Are Section"),

		MultiFieldPanel([
			FieldPanel('services_image'),
			FieldPanel('services_text')
		], heading="Services Section")


	]

	template = 'core/aboutus_page.html'

	page_title = 'About Us'
	page_slug = 'about-us'


class SlideBlock(StructBlock):
	image = ImageChooserBlock(required=True)
	text = TextBlock()
	button = CharBlock(required=True, max_length=20)
	url = CharBlock(required=True, max_length=100)

	class Meta:
		template = 'core/webcontents/slide.html'

class HomePage(MenuPage):

	slideshows = StreamField([
		('slides', SlideBlock())
	])

	content_panels = [
		StreamFieldPanel('slideshows')
	]

	template = 'core/home_page.html'

	page_title = 'Home'
	page_slug = 'home'

	def get_context(self, request, *args, **kwargs):
		from .models import Item, Category
		context = super().get_context(request, *args, **kwargs)

		context['new_releases'] = Item.get_new_releases(3)
		context['categories'] = list(Category.objects.all())
		random.shuffle(context['categories'])
		context['categories'] = context['categories'][:10]

		context['items'] = list(Item.objects.all())
		random.shuffle(context['items'])
		context['items'] = context['items'][:10]
		
		return context

ALLOWED_SUBPAGES = {
	
}