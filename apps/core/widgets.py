from django.forms import widgets

from .models import ItemColor, ItemSize

class ColorRadioWidget(widgets.RadioSelect):
	template_name = 'django/forms/widgets/custom_widgets/radio.html'
	option_template_name = 'django/forms/widgets/custom_widgets/color_radio_option.html'

	def create_option(self, *args, **kwargs):
		option = super().create_option(*args, **kwargs)
		option['color'] = ItemColor.objects.get(pk=option['value'])
		return option


class SizeRadioWidget(widgets.RadioSelect):
	template_name = 'django/forms/widgets/custom_widgets/radio.html'
	option_template_name = 'django/forms/widgets/custom_widgets/size_radio_option.html'

	def create_option(self, *args, **kwargs):
		option = super().create_option(*args, **kwargs)
		option['size'] = ItemSize.objects.get(pk=option['value'])
		return option