from datetime import timezone

import django_filters
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import Q
from django import forms
from internationalflavor.vat_number.validators import VATNumberValidator

from django.conf import settings
from users.models import AppUser


class Supplier(models.Model):
    DELIVERY_METHOD_CHOICES = [
        ('delivery', 'На място'),
        ('pickup', 'Вземане'),
    ]
    name = models.CharField(
        max_length=50,
        unique=True,
        blank=True,
        null=True,
        verbose_name="Име"
    )

    vat_number = models.CharField(
        max_length=20,
        blank=True,
        null=True,
        verbose_name="ДДС номер"
    )

    email = models.EmailField(
        max_length=50,
        unique=True,
        blank=True,
        null=True
    )

    phone = models.CharField(
        max_length=20,
        blank=True,
        null=True,
        verbose_name="Телефон"
    )

    contact_person = models.CharField(
        max_length=30,
        blank=True,
        null=True,
        verbose_name="Лице за контакт"
    )

    delivery_method = models.CharField(
        max_length=20,
        choices=DELIVERY_METHOD_CHOICES,
        default='delivery',
        verbose_name="Метод на доставка"
    )

    responsible_logistic = models.ForeignKey(
        AppUser,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        limit_choices_to=Q(groups__name='Logistics') | Q(groups__name='Logistics Manager'),
        related_name='suppliers_responsible',
        verbose_name="Отговорен логистик"

    )
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

    def clean(self):
        if self.responsible_logistic:
            user_groups = self.responsible_logistic.groups.values_list('name', flat=True)
            if 'Logistics' not in user_groups and 'Logistics Manager' not in user_groups:
                raise ValidationError("Отговорният логистик трябва да е с роля логистик или логистичен мениджър.")


class Contract(models.Model):
    CONTRACT_TYPE_CHOICES = [
        ('supply', 'Стоки'),
        ('service', 'Услуги'),
        ('other', 'Други'),
    ]

    ACTIVE_CHOICES = [
        ('', 'Всички'),
        ('yes', 'Да'),
        ('no', 'Не'),
    ]

    supplier = models.ForeignKey(
        'Supplier',
        on_delete=models.CASCADE,
        verbose_name="Доставчик"
    )
    contract_type = models.CharField(
        max_length=20,
        choices=CONTRACT_TYPE_CHOICES,
        default='supply',
        verbose_name="Тип"
    )

    signed_date = models.DateField(
        verbose_name="Дата на подписване"
    )

    expiry_date = models.DateField(
        verbose_name="Дата на изтичане",
        null=True,
        blank=True
    )

    file = models.FileField(
        upload_to='contracts/',
        verbose_name="Файл"
    )

    @property
    def is_active_dynamic(self):
        if self.expiry_date and self.expiry_date < timezone.now().date():
            return False
        return True

    is_active = models.BooleanField(default=True, verbose_name="Активен")

    def __str__(self):
        return f"Договор {self.contract_type} – {self.supplier.name} ({self.is_active})"


class DeliverySchedule(models.Model):
    DAYS_OF_WEEK = [
        ('mon', 'Monday'),
        ('tue', 'Tuesday'),
        ('wed', 'Wednesday'),
        ('thu', 'Thursday'),
        ('fri', 'Friday'),
    ]

    TIME_SLOTS = [
        ('08-10', '08:00-10:00'),
        ('10-12', '10:00-12:00'),
        ('12-14', '12:00-14:00'),
        ('14-16', '14:00-16:00'),
    ]

    day = models.CharField(max_length=3, choices=DAYS_OF_WEEK)
    time_slot = models.CharField(max_length=5, choices=TIME_SLOTS)
    supplier = models.ForeignKey('suppliers.Supplier', on_delete=models.CASCADE, related_name='delivery_schedules')
    logistics_responsible = models.ForeignKey('suppliers.Supplier', on_delete=models.CASCADE, related_name='logistics_schedules')
    note = models.CharField(max_length=150, blank=True)

    class Meta:
        unique_together = ('day', 'time_slot', 'supplier')

    def __str__(self):
        return f"{self.get_day_display()} {self.get_time_slot_display()} - {self.supplier}"
