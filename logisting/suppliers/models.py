from django.conf import settings
from django.db import models

from core.validators import phone_validator, validate_vat_by_country


class Supplier(models.Model):
    DELIVERY = "delivery"
    PICKUP = "pickup"
    COURIER = "courier"

    DELIVERY_METHOD_CHOICES = [
        (DELIVERY, "Delivery"),
        (PICKUP, "Pickup"),
        (COURIER, "Courier"),
    ]

    company_name = models.CharField(max_length=50)

    vat_number = models.CharField(max_length=30, blank=True)
    country = models.CharField(max_length=30, default="Bulgaria")
    city = models.CharField(max_length=80, blank=True)
    address = models.CharField(max_length=255, blank=True)

    email = models.EmailField(blank=True)

    phone = models.CharField(
        max_length=16,
        blank=True,
        validators=[phone_validator],
        help_text="Format: +359888123456",
    )

    contact_person = models.CharField(max_length=50, blank=True)

    delivery_method = models.CharField(
        max_length=20,
        choices=DELIVERY_METHOD_CHOICES,
        default=DELIVERY,
    )

    is_active = models.BooleanField(default=True)

    responsible_logistician = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="suppliers",
    )

    notes = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["company_name"]
        verbose_name = "Supplier"
        verbose_name_plural = "Suppliers"

    def __str__(self):
        return self.company_name

    def clean(self):
        super().clean()

        # Нормализация на телефона
        # 0888123456 -> +359888123456
        if self.phone and not self.phone.startswith("+"):
            self.phone = "+359" + self.phone.lstrip("0")

        # VAT validation by country
        if self.vat_number:
            validate_vat_by_country(self.vat_number, self.country)

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)