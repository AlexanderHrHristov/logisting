from django.contrib import admin
from .models import AppUser

@admin.register(AppUser)
class AppUserAdmin(admin.ModelAdmin):
    list_display = (
        'username', 'email', 'is_staff',
        'is_driver', 'is_transport_manager',
        'is_logistics', 'is_logistics_manager',
        'is_warehouseman',
    )
    list_filter = (
        'is_staff',
        'is_driver',
        'is_transport_manager',
        'is_logistics',
        'is_logistics_manager',
        'is_warehouseman',
    )
    search_fields = ('username', 'email')
    ordering = ('username',)
