from django.contrib.auth.models import AbstractUser
from django.db import models


class AppUser(AbstractUser):
    """
    Custom user model that extends the default Django user model.
    """
    # Роли
    is_logistics = models.BooleanField(default=False)
    is_logistics_manager = models.BooleanField(default=False)
    is_driver = models.BooleanField(default=False)
    is_transport_manager = models.BooleanField(default=False)
    is_warehouseman = models.BooleanField(default=False)
    is_dealer = models.BooleanField(default=False)

    # Допълнителни данни
    phone = models.CharField(max_length=20, blank=True, null=True, verbose_name="Телефон")
    position = models.CharField(max_length=50, blank=True, null=True, verbose_name="Длъжност")
    created_by_admin = models.BooleanField(default=False, verbose_name="Създаден от админ")
    notes = models.TextField(blank=True, null=True, verbose_name="Бележки")

    def __str__(self):
        return f"{self.username} ({self.get_full_name()})"
