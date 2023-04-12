from django.db import models

from secrets import token_hex

from . import webcontents


def get_random_hex():
	return token_hex(16)


class Category(models.Model):
	name = models.CharField(max_length=50)
	image = models.ImageField(upload_to='core/categories/')
	parent_category = models.ForeignKey('Category', on_delete=models.CASCADE, null=True, blank=True)

	def __str__(self):
		return self.name
	
	def is_parent(self):
		return Category.objects.all().filter(parent_category=self).exists()
	
	def get_heirarchy(self):
		heirarchy = [self]
		if(self.parent_category):
			heirarchy = [self] + self.parent_category.get_heirarchy()
		
		return heirarchy
	

class ItemColor(models.Model):
	name = models.CharField(max_length=50)
	hex_value = models.CharField(max_length=10, null=True, blank=True)
	
	def __str__(self):
		return '{} - {}'.format(self.name, self.hex_value)


class ItemSize(models.Model):
	value = models.CharField(max_length=50)

	def __str__(self):
		return '{}'.format(self.value)


class Item(models.Model):
	name = models.CharField(max_length=50)
	category = models.ForeignKey(Category, on_delete=models.CASCADE)
	cover_image = models.ImageField(upload_to='core/items/covers/')
	price = models.DecimalField(max_digits=6, decimal_places=2)
	description = models.TextField()
	colors = models.ManyToManyField(ItemColor)
	sizes = models.ManyToManyField(ItemSize)

	release_datetime = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return self.name
	
	def get_images(self):
		return [image.image for image in ItemImage.objects.filter(item=self)]
	
	def get_heirarchy(self):
		return [self] + self.category.get_heirarchy()
	
	def get_price(self):
		return '{} Birr'.format(self.price)

	def get_colors(self):
		return self.colors.all()

	def get_sizes(self):
		return self.sizes.all()

	@staticmethod
	def get_new_releases(num):
		return Item.objects.all().order_by('-release_datetime')[:num]


class ItemImage(models.Model):
	item = models.ForeignKey(Item, on_delete=models.CASCADE)
	image = models.ImageField(upload_to="core/item/images/")
	def __str__(self):
		return '{} - {}'.format(self.image.url, self.item.name)


class Cart(models.Model):
	id = models.CharField(primary_key=True, default=get_random_hex, editable=False, max_length=32)
	ordered = models.BooleanField(default=False)
	done = models.BooleanField(default=False)

	def get_orders(self):
		return Order.objects.all().filter(cart=self)
	
	def get_total_price(self):
		return "{} Birr".format(sum([float(order.get_price()) for order in self.get_orders()]))

	@staticmethod
	def get_or_create(request):
		if(request.session.get('cart_id')):
			return Cart.objects.get(pk=request.session.get('cart_id'))
		cart = Cart.objects.create()
		request.session['cart_id'] = cart.id
		return cart


class Order(models.Model):
	id = models.CharField(primary_key=True, default=get_random_hex, editable=False, max_length=32)
	item = models.ForeignKey(Item, on_delete=models.CASCADE)
	quantity = models.IntegerField()
	color = models.ForeignKey(ItemColor, on_delete=models.CASCADE)
	size = models.ForeignKey(ItemSize, on_delete=models.CASCADE)
	cart = models.ForeignKey(Cart, on_delete=models.CASCADE)


	def get_price(self):
		return '{:.2f}'.format(self.item.price * self.quantity)


class ContactMessage(models.Model):
	sender = models.CharField(max_length=100)
	email = models.EmailField()
	phone_number = models.CharField(max_length=20)
	subject = models.CharField(max_length=150)
	message = models.TextField()