from django.core.exceptions import ValidationError
from django.db import models
from users.models import AppUser


class ExternalWarehouse(models.Model):
    date = models.DateField()  # дата на запис
    supplier = models.CharField("Доставчик", max_length=30)
    location = models.CharField("Локация", max_length=30)
    volume = models.DecimalField("Обем", max_digits=3, decimal_places=1)
    thermolabile = models.BooleanField("Термолабилни")
    narcotic = models.BooleanField("Наркотични")
    note = models.TextField("Забележка", blank=True, null=True)
    driver = models.CharField("Към Транспорт", max_length=100)
    received = models.BooleanField("Получено", default=False)

    def __str__(self):
        return f"{self.date} - {self.supplier} - {self.location}"


class Supplier(models.Model):
    DELIVERS_CHOICES = [
        ('yes', 'Да'),
        ('no', 'Не'),
    ]
    name = models.CharField(max_length=50, unique=True, blank=True, null=True)
    email = models.EmailField(max_length=50, unique=True, blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True, verbose_name="Телефон")
    contact_person = models.CharField(max_length=30, blank=True, null=True)
    delivers_to_us = models.CharField(choices=DELIVERS_CHOICES, max_length=3, blank=False, null=False)
    responsible_logistic = models.ForeignKey(
        AppUser,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        limit_choices_to=models.Q(is_logistics=True) | models.Q(is_logistics_manager=True),
        related_name='suppliers_responsible'
    )
    is_active = models.BooleanField(default=True)

    def clean(self):
        if self.responsible_logistic and not (
            self.responsible_logistic.is_logistics or self.responsible_logistic.is_logistics_manager
        ):
            raise ValidationError("Отговорният логистик трябва да е с роля логистик или логистичен мениджър.")
