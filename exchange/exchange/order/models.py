from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from vouchers.models import Voucher


class Order(models.Model):
    token = models.CharField(max_length=255, blank=True)
    total = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="Order Total (€)"
    )
    emailAddress = models.EmailField(
        max_length=255,
        blank=True,
        verbose_name="Customer Email"
    )
    created = models.DateTimeField(auto_now_add=True)

    billingName = models.CharField(max_length=255, blank=True)
    billingAddress1 = models.CharField(max_length=255, blank=True)
    billingCity = models.CharField(max_length=255, blank=True)
    billingPostcode = models.CharField(max_length=20, blank=True)
    billingCountry = models.CharField(max_length=200, blank=True)

    shippingName = models.CharField(max_length=255, blank=True)
    shippingAddress1 = models.CharField(max_length=255, blank=True)
    shippingCity = models.CharField(max_length=255, blank=True)
    shippingPostcode = models.CharField(max_length=20, blank=True)
    shippingCountry = models.CharField(max_length=200, blank=True)

    voucher = models.ForeignKey(
        Voucher,
        related_name="tennis_orders",
        null=True,
        blank=True,
        on_delete=models.SET_NULL
    )
    discount = models.IntegerField(
        default=0,
        validators=[MinValueValidator(0), MaxValueValidator(100)]
    )

    class Meta:
        db_table = "tennis_order"
        ordering = ["-created"]

    def __str__(self):
        return f"Order #{self.id}"


class OrderItem(models.Model):
    product = models.CharField(max_length=255)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="Price (€)"
    )
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")

    class Meta:
        db_table = "tennis_order_item"

    def sub_total(self):
        return self.quantity * self.price

    def __str__(self):
        return f"{self.quantity} × {self.product}"


