from django.contrib import admin
from .models import Product, Order, OrderItem

# Register your models here.

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    """
    Product model in the Django admin.
    """
    list_display = ('name', 'price_per_kg', 'stock_in_kg')
    search_fields = ('name',)
    list_filter = ('stock_in_kg',)
    ordering = ('name',)

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'created_at', 'total')
    date_hierarchy = 'created_at'
    ordering = ('-created_at',)
    readonly_fields = ('created_at', 'total')
    inlines = []

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('order', 'product', 'quantity', 'price_per_kg')
    search_fields = ('product__name', 'order__id')
    list_filter = ('product',)
    ordering = ('order',)
