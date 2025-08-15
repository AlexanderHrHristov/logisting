from django.contrib.auth import get_user_model
from django.db import models

from suppliers.models import Supplier

User = get_user_model()

class Order(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Изпратена'),
        ('confirmed', 'Потвърдена'),
        ('delivered', 'Доставена'),
    ]

    supplier = models.ForeignKey(
        Supplier, 
        on_delete=models.CASCADE, 
        related_name='orders',
        verbose_name='Доставчик',
        help_text='Изберете доставчик',
        )
    
    order_date = models.DateField(
        verbose_name='Дата на поръчка',
        help_text='Изберете дата',
    )

    status = models.CharField(
        max_length=20, 
        choices=STATUS_CHOICES, 
        default='pending',
        verbose_name='Статус',
        help_text='Изберете статус на поръчката',
        )
    
    note = models.TextField(
        blank=True,
        verbose_name='Бележка',
        help_text='Допълнителна информация за поръчката',
        )
    
    created_by = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True)

    class Meta:
        ordering = ['-order_date']

    def __str__(self):
        return f"Поръчка към {self.supplier.name} на {self.order_date}"
