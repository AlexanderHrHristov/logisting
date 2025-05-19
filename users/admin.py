from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import AppUser


@admin.register(AppUser)
class CustomUserAdmin(UserAdmin):
    model = AppUser
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_logistics', 'is_driver', 'is_warehouseman')
    list_filter = ('is_logistics', 'is_driver', 'is_warehouseman', 'is_logistics_manager', 'is_transport_manager', 'is_dealer')

    fieldsets = UserAdmin.fieldsets + (
        ('Допълнителна информация', {
            'fields': ('phone', 'position', 'created_by_admin', 'notes',
                       'is_logistics', 'is_logistics_manager', 'is_driver',
                       'is_transport_manager', 'is_warehouseman', 'is_dealer'),
        }),
    )

    search_fields = ('username', 'email')
    ordering = ('username',)
