from django.contrib import admin
from .models import OnSiteDelivery, PickupDelivery

admin.site.register(OnSiteDelivery)
admin.site.register(PickupDelivery)
