from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import Q

from users.models import AppUser


class Supplier(models.Model):
    DELIVERY_METHOD_CHOICES = [
        ('delivery', 'Доставка'),
        ('pickup', 'Ние вземаме'),
    ]
    name = models.CharField(
        max_length=50,
        unique=True,
        blank=True,
        null=True,
        verbose_name="Име"
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

    def clean(self):
        if self.responsible_logistic:
            user_groups = self.responsible_logistic.groups.values_list('name', flat=True)
            if 'Logistics' not in user_groups and 'Logistics Manager' not in user_groups:
                raise ValidationError("Отговорният логистик трябва да е с роля логистик или логистичен мениджър.")
