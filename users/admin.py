from django.contrib import admin
from .models import AppUser


@admin.register(AppUser)
class AppUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'is_active', 'is_staff', 'date_joined')
    list_filter = ('is_active', 'is_staff', 'is_superuser')
    search_fields = ('username', 'email')
    ordering = ('-date_joined',)
    list_per_page = 20
    readonly_fields = ('date_joined',)
    actions = ['deactivate_selected_users']

    def deactivate_selected_users(self, request, queryset):
        updated = queryset.update(is_active=False)
        self.message_user(request, f"{updated} потребителя бяха деактивирани успешно.")
    deactivate_selected_users.short_description = "Деактивирай избраните потребители"
