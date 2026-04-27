from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import Q

from suppliers.models import Supplier

class DeliveryStatus(models.TextChoices):
    PLANNED = "planned", "Планирана"
    CONFIRMED = "confirmed", "Потвърдена"
    ARRIVED = "arrived", "Пристигнала"
    COMPLETED = "completed", "Завършена"
    CANCELLED = "cancelled", "Отказана"


class DeliverySchedule(models.Model):
    supplier = models.ForeignKey(
        Supplier,
        on_delete=models.PROTECT,
        related_name="deliveries",
        verbose_name="Доставчик",
    )

    date = models.DateField(
        verbose_name="Дата",
    )

    hour = models.TimeField(
        verbose_name="Час",
    )

    pallets = models.DecimalField(
        max_digits=5,
        decimal_places=1,
        default=0,
        verbose_name="Палети",
    )

    thermolabile = models.BooleanField(
        default=False,
        verbose_name="Термолабилни",
    )

    narcotic = models.BooleanField(
        default=False,
        verbose_name="Наркотични",
    )

    status = models.CharField(
        max_length=20,
        choices=DeliveryStatus.choices,
        default=DeliveryStatus.PLANNED,
        verbose_name="Статус",
    )

    logistics_responsible = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="deliveries_responsible",
        limit_choices_to=Q(groups__name="Logistics") | Q(groups__name="Logistics Manager"),
        verbose_name="Отговорен логистик",
    )

    note = models.TextField(
        blank=True,
        verbose_name="Забележка",
    )

    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="deliveries_created",
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    MAX_PER_HOUR = 8

    class Meta:
        ordering = ["date", "hour"]
        verbose_name = "Доставка"
        verbose_name_plural = "Доставки"
        constraints = [
            models.UniqueConstraint(
                fields=["supplier", "date", "hour"],
                name="unique_supplier_delivery_per_hour",
            )
        ]

    def clean(self):
        qs = DeliverySchedule.objects.filter(
            date=self.date,
            hour=self.hour,
        )

        if self.pk:
            qs = qs.exclude(pk=self.pk)

        if qs.count() >= self.MAX_PER_HOUR:
            raise ValidationError(
                f"Максимум {self.MAX_PER_HOUR} доставки за този час."
            )

    def __str__(self):
        return f"{self.date} {self.hour:%H:%M} – {self.supplier.company_name}"
    
class PickupStatus(models.TextChoices):
    PLANNED = "planned", "Планирано"
    READY = "ready", "Готово"
    PICKED_UP = "picked_up", "Взето"
    CANCELLED = "cancelled", "Отказано"


class PickupSchedule(models.Model):
    supplier = models.ForeignKey(
        Supplier,
        on_delete=models.PROTECT,
        related_name="pickups",
        limit_choices_to=Q(delivery_method="pickup"),
        verbose_name="Доставчик",
    )

    date = models.DateField(
        verbose_name="Дата",
    )

    volume = models.DecimalField(
        max_digits=5,
        decimal_places=1,
        default=0,
        verbose_name="Палети",
    )

    thermolabile = models.BooleanField(
        default=False,
        verbose_name="Термолабилни",
    )

    narcotic = models.BooleanField(
        default=False,
        verbose_name="Наркотични",
    )

    driver = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="pickups_assigned",
        limit_choices_to=Q(groups__name="Drivers"),
        verbose_name="Шофьор",
    )

    status = models.CharField(
        max_length=20,
        choices=PickupStatus.choices,
        default=PickupStatus.PLANNED,
        verbose_name="Статус",
    )

    note = models.TextField(
        blank=True,
        verbose_name="Забележка",
    )

    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="pickups_created",
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["date", "supplier"]
        verbose_name = "Вземане"
        verbose_name_plural = "Вземания"

    def __str__(self):
        return f"{self.date} – {self.supplier.company_name}"