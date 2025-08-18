from django.contrib.auth.models import AbstractUser
from django.db import models


class AppUser(AbstractUser):
    """
    Custom user model that extends the default Django user model.
    """

    # Допълнителни данни
    username = models.CharField(
        max_length=30,  # <- нова дължина
        unique=True,
        verbose_name="Username",
        help_text="Required. 30 characters or fewer. Letters, digits and @/./+/-/_ only.",
        error_messages={
            "unique": "A user with that username already exists.",
        },
    )
    phone = models.CharField(
        max_length=20, 
        blank=True, 
        null=True, 
        verbose_name="Телефон"
        )
    position = models.CharField(
        max_length=50, 
        blank=True, 
        null=True, 
        verbose_name="Длъжност"
        )
    created_by_admin = models.BooleanField(
        default=False, 
        verbose_name="Създаден от админ"
        )
    notes = models.TextField(
        blank=True, 
        null=True, 
        verbose_name="Бележки"
        )

    def __str__(self):
        return f"{self.get_full_name()}"
    