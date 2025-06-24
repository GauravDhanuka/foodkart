from django.db import migrations
from decimal import Decimal

def create_initial_products(apps, schema_editor):
    """
    Populates the Product model with initial data.
    This function is run during the migration.
    """
    Product = apps.get_model('cart', 'Product')

    products_data = [
        {"name": "Potatoes", "price_per_kg": Decimal('5.00'), "stock_in_kg": Decimal('100.00')},
        {"name": "Carrots", "price_per_kg": Decimal('4.00'), "stock_in_kg": Decimal('50.00')},
        {"name": "Onions", "price_per_kg": Decimal('2.00'), "stock_in_kg": Decimal('75.00')},
    ]

    for data in products_data:
        Product.objects.get_or_create(
            name=data["name"],
            defaults={
                "price_per_kg": data["price_per_kg"],
                "stock_in_kg": data["stock_in_kg"]
            }
        )

def reverse_initial_products(apps, schema_editor):
    """
    Reverses the population by deleting the initial product data.
    This function is run if the migration is unapplied (e.g., during `migrate zero`).
    """
    Product = apps.get_model('cart', 'Product')
    product_names = [
        "Potatoes",
        "Carrots",
        "Onions",
    ]
    Product.objects.filter(name__in=product_names).delete()


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(create_initial_products, reverse_initial_products),
    ]