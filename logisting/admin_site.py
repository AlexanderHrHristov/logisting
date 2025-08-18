from django.contrib.admin import AdminSite
from suppliers.models import Supplier, Contract
from suppliers.admin import SupplierAdmin, ContractAdmin
from users.models import AppUser
from users.admin import AppUserAdmin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import GroupAdmin


class CustomAdminSite(AdminSite):
    site_header = "Logisting Admin"
    site_title = "Logisting Admin Portal"
    index_title = "Добре дошли в LogiSting Admin панел"

    def has_permission(self, request):
        return request.user.is_active and request.user.is_superuser

    def get_app_list(self, request):
        app_dict = super()._build_app_dict(request)
        allowed_apps = ['auth', 'users', 'suppliers']
        filtered_apps = [app for app in app_dict.values() if app['app_label'] in allowed_apps]
        return sorted(filtered_apps, key=lambda x: x['name'].lower())


custom_admin_site = CustomAdminSite(name='custom_admin')

# Регистрираме моделите с нашите персонализирани Admin класове
custom_admin_site.register(AppUser, AppUserAdmin)
custom_admin_site.register(Group, GroupAdmin)
custom_admin_site.register(Supplier, SupplierAdmin)
custom_admin_site.register(Contract, ContractAdmin)
