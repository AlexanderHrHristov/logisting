from django.contrib import admin

from .models import Supplier, SupplierContract


@admin.register(Supplier)
class SupplierAdmin(admin.ModelAdmin):
    list_display = (
        "company_name",
        "vat_number",
        "email",
        "phone",
        "delivery_method",
        "responsible_logistician",
        "is_active",
    )
    list_filter = ("delivery_method", "is_active")
    search_fields = ("company_name", "vat_number", "email", "phone", "contact_person")


@admin.register(SupplierContract)
class SupplierContractAdmin(admin.ModelAdmin):
    list_display = (
        "supplier",
        "contract_type",
        "contract_number",
        "signed_date",
        "expiry_date",
        "is_active",
        "is_expired",
        "is_currently_active",
    )
    list_filter = ("contract_type", "is_active", "signed_date", "expiry_date")
    search_fields = (
        "supplier__company_name",
        "contract_number",
        "document_type",
    )
