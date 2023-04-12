from django.contrib import admin

from wagtail.contrib.modeladmin.options import ModelAdmin, ModelAdminGroup, modeladmin_register

from . import models, webcontents


admin.site.register(webcontents.Tab)
admin.site.register(webcontents.ContactInformation)
admin.site.register(webcontents.SocialMedia)
admin.site.register(webcontents.PickupLocation)

admin.site.register(models.Category)
admin.site.register(models.Item)
admin.site.register(models.ItemImage)
admin.site.register(models.ItemColor)
admin.site.register(models.ItemSize)



class ItemModelAdmin(ModelAdmin):
	model = models.Item
	menu_label = 'Items'
	menu_icon = 'tag'
	list_display = ('name', 'category', 'description')
	list_filter = ('category',)
	search_fields = ('name', 'description', 'price')


class ItemImageModelAdmin(ModelAdmin):
	model = models.ItemImage
	menu_label = "Images"
	menu_icon = 'image'
	list_display = ('image', 'item')
	list_filter = ('item',)
	search_fields =  ('image',)


class ItemColorModelAdmin(ModelAdmin):
	model = models.ItemColor
	menu_label = "Colors"
	menu_icon = "radio-full"
	list_display = ("name", "hex_value")
	list_filter = ("name", )
	search_fields = ("hex",)


class ItemSizeModelAdmin(ModelAdmin):
	model = models.ItemSize
	menu_label = "Sizes"
	menu_icon = 'order'
	list_display = ("value",)
	list_filter = ()
	search_fields = ("value",)


class CategoryModelAdmin(ModelAdmin):
	model = models.Category
	menu_label = 'Categories'
	menu_icon = 'folder-open-inverse'
	list_display = ('name', 'parent_category')
	list_filter = ('parent_category',)
	search_fields = ('name',)


class ItemsModelAdminGroup(ModelAdminGroup):
	menu_label = 'Items'
	menu_order = 300
	menu_icon = 'folder-open-inverse'
	items = (CategoryModelAdmin, ItemModelAdmin, ItemImageModelAdmin, ItemColorModelAdmin, ItemSizeModelAdmin)

modeladmin_register(ItemsModelAdminGroup)