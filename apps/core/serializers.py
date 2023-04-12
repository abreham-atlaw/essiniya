from rest_framework import serializers

from .models import Cart, Order, ItemColor, ItemSize, Item


class ColorSerializer(serializers.ModelSerializer):

	class Meta:
		model = ItemColor
		fields = '__all__'


class ItemSizeSerializer(serializers.ModelSerializer):

	class Meta:
		model = ItemSize
		fields = '__all__'


class ItemSerializer(serializers.ModelSerializer):

	class Meta:
		model = Item
		exclude = ('colors', 'sizes')

class OrderSerializer(serializers.ModelSerializer):
	color = ColorSerializer(read_only=True, many=False)
	size = ItemSizeSerializer(read_only=True, many=False)
	item = ItemSerializer(read_only=True, many=False)
	price = serializers.CharField(read_only=True, source='get_price')

	class Meta:
		model = Order
		fields = '__all__'


class CartSerializer(serializers.ModelSerializer):
	orders = OrderSerializer(read_only=True, many=True, source='get_orders')
	price = serializers.CharField(read_only=True, source='get_total_price')
	class Meta:
		model = Cart
		fields = '__all__'
		read_only_fields = ('orders', 'ordered')