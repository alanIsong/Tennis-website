from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone


class Voucher(models.Model):
    code = models.CharField(max_length=50, unique=True)
    valid_from = models.DateTimeField()
    valid_to = models.DateTimeField()
    discount = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        help_text="Enter a percentage value between 0 and 100.",
    )
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ["-valid_from"]
        verbose_name = "Voucher"
        verbose_name_plural = "Vouchers"

    def __str__(self):
        return f"{self.code} ({self.discount}% off)"

    def is_valid(self):
        """Check if voucher is currently valid."""
        now = timezone.now()
        return self.active and self.valid_from <= now <= self.valid_to


