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

class Order(models.Model):
    """
    Purchase Order (purchase history entry).
    """
    created_at = models.DateTimeField(auto_now_add=True)
    total = models.DecimalField(max_digits=12, decimal_places=2)

    def __str__(self):
        return f"Order #{self.id} at {self.created_at.strftime('%Y-%m-%d %H:%M:%S')}"

class OrderItem(models.Model):
    """
    Product in an Order.
    """
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    quantity = models.DecimalField(max_digits=10, decimal_places=2)
    price_per_kg = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.quantity} kg {self.product.name} in Order #{self.order.id}"