# logisting/admin_site.py
from django.contrib.admin import AdminSite
from django.contrib.auth.models import User, Group
from django.contrib import admin
from users.models import AppUser
from suppliers.models import Supplier, Contract  # твоите модели


class CustomAdminSite(AdminSite):
    site_header = "Logisting Admin"
    site_title = "Logisting Admin Portal"
    index_title = "Добре дошли в Logisting Admin"

    def has_permission(self, request):
        return request.user.is_active and request.user.is_superuser

    def get_app_list(self, request):
        app_dict = super()._build_app_dict(request)
        allowed_apps = ['auth', 'users', 'suppliers']
        filtered_apps = [app for app in app_dict.values() if app['app_label'] in allowed_apps]
        return sorted(filtered_apps, key=lambda x: x['name'].lower())

custom_admin_site = CustomAdminSite(name='custom_admin')

custom_admin_site.register(AppUser, admin.ModelAdmin)
custom_admin_site.register(Supplier, admin.ModelAdmin)
custom_admin_site.register(Contract, admin.ModelAdmin)
