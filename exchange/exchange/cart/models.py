from django.db import models
from shop.models import Product


class Cart(models.Model):
    cart_id = models.CharField(max_length=255, blank=True, unique=False)
    date_created = models.DateField(auto_now_add=True)

    class Meta:
        db_table = "tennis_cart"
        ordering = ["-date_created"]

    def __str__(self):
        return f"Cart {self.cart_id}"


class CartItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name="items")
    quantity = models.PositiveIntegerField(default=1)
    active = models.BooleanField(default=True)

    class Meta:
        db_table = "tennis_cart_item"

    def sub_total(self):
        return self.product.price * self.quantity

    def __str__(self):
        return f"{self.quantity} x {self.product}"
