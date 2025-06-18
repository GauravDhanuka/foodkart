from django.db import models

# Create your models here.

class Product(models.Model):
    """
    Products in Inventory
    """

    name = models.CharField(unique=True, max_length=100)
    price_per_kg = models.DecimalField(max_digits=10, decimal_places=2)
    stock_in_kg = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        verbose_name = 'Product'
        verbose_name_plural = 'Products'
        ordering = ['name']

    def __str__(self):
        """
        String representation of Product Object
        """

        return f"{self.name} ({self.stock_in_kg} kg in stock)"