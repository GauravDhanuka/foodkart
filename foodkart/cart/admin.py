from django.contrib import admin
from models import Product

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
