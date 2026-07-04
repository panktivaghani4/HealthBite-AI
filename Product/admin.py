from django.contrib import admin
from .models import Product, Order


class ProductAdmin(admin.ModelAdmin):
    list_display = [
        'category',
        'name',
        'price',
        'calories',
        'protein',
        'carbs',
        'fat',
        'food_type',
        'created',
        'last_updated'
    ]

    readonly_fields = [
        'slug',
        'created',
        'last_updated'
    ]

    search_fields = [
        'name',
        'category'
    ]

    list_filter = [
        'category',
        'food_type'
    ]


admin.site.register(Product, ProductAdmin)


class OrderAdmin(admin.ModelAdmin):

    list_display = [
        'product',
        'count',
        'cost',
        'order_by',
        'name',
        'status',          # NEW
        'delivered',
        'delivered_on',
        'created',
        'last_updated'
    ]

    readonly_fields = [
        'slug',
        'order_by',
        'created',
        'last_updated'
    ]

    list_filter = [
        'status',
        'delivered',
        'created'
    ]

    search_fields = [
        'name',
        'contact',
        'product__name'
    ]

    list_editable = [
        'status'
    ]


admin.site.register(Order, OrderAdmin)