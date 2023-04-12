from django import forms
from django.core.mail import EmailMessage

from .models import ItemSize, Order, ContactMessage#, Cart
from . import widgets
from KingsWay import settings


class AddToCartForm(forms.Form):
	size = forms.ModelChoiceField(queryset=None, empty_label=None, widget=widgets.SizeRadioWidget())
	color = forms.ModelChoiceField(queryset=None, empty_label=None, widget=widgets.ColorRadioWidget())
	quantity = forms.IntegerField(min_value=1, initial=1, max_value=6)

	def __init__(self, *args, order=None, item=None, **kwargs):
		super().__init__(*args, **kwargs)
		
		self.item = item
		self.order = order

		self.fields['size'].queryset = self.item.get_sizes()
		self.fields['color'].queryset = self.item.get_colors()

		if(self.order):
			self.set_initials()

	def set_initials(self):
		self.fields['size'].initial = self.order.size
		self.fields['quantity'].initial = self.order.quantity
		self.fields['color'].initial = self.order.color

	def add_to_cart(self, cart):
		print(self.cleaned_data)
		order = Order.objects.create(
			item = self.item,
			quantity = self.cleaned_data.get('quantity'),
			size = self.cleaned_data.get('size'),
			color = self.cleaned_data.get('color'),
			cart = cart
		)

	def edit_order(self):
		print(self.cleaned_data)
		self.order.quantity = self.cleaned_data.get('quantity')
		self.order.size = self.cleaned_data.get('size')
		self.order.color = self.cleaned_data.get('color')
		self.order.save()


class ContactUsForm(forms.Form):
	full_name = forms.CharField()
	email = forms.EmailField()
	phone_number = forms.CharField()
	subject = forms.CharField()
	message = forms.CharField(widget=forms.Textarea())

	def clean_full_name(self):
		data = self.cleaned_data["full_name"]
		if(data.count(' ') < 1):
			raise forms.ValidationError('Please enter your FULL name.')

		return data

	def clean_phone_number(self):
		data = self.cleaned_data["phone_number"]
		
		if not data[0] == '+':
			raise forms.ValidationError('Please include country code in your phone number.')

		if len(data) < 5 or not data[1:].isnumeric():
			raise forms.ValidationError('Please enter a valid phone number.')

		return data
	
	def send_message(self):
		message = ContactMessage.objects.create(
			sender = self.cleaned_data.get('full_name'),
			email = self.cleaned_data.get('email'),
			phone_number = self.cleaned_data.get('phone_number'),
			subject = self.cleaned_data.get('subject'),
			message = self.cleaned_data.get('message')
		)

		email_body = '{}\n\n\nSender Info:\nName = {}\nPhone Number = {}\nE-Mail = {}'.format(
			message.message, message.sender, message.phone_number, message.email
		)
		email = EmailMessage(message.subject, email_body, settings.EMAIL_HOST_USER, [settings.EMAIL_APPLICATION_RECIEVER_EMAIL])
		email.send()