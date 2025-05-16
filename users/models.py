from django.contrib.auth.models import AbstractUser
from django.db import models

class AppUser(AbstractUser):
    """
    Custom user model that extends the default Django user model.
    """
    is_logistics = models.BooleanField(default=False)
    is_logistics_manager = models.BooleanField(default=False)
    is_driver = models.BooleanField(default=False)
    is_transport_manager = models.BooleanField(default=False)
    is_warehouseman = models.BooleanField(default=False)

    # Add any additional fields you want to include in your custom user model
    # For example, you can add a profile picture field:
    # profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)

    def __str__(self):
        return self.username

