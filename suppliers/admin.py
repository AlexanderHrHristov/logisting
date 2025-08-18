from django.contrib import admin

# ----------------------------
class SupplierAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "vat_number",
        "email",
        "phone",
        "contact_person",
        "delivery_method",
        "responsible_logistic",
        "is_active",
    )
    list_filter = ("delivery_method", "is_active", "responsible_logistic")
    list_editable = ("is_active",)
    ordering = ("name",)
    search_fields = ("name", "contact_person", "email", "phone")


class ContractAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "supplier",
        "contract_type",
        "signed_date",
        "expiry_date",
        "file",
    )
    list_filter = (
        "contract_type",
        ("signed_date", admin.DateFieldListFilter),
        ("expiry_date", admin.DateFieldListFilter),
    )
    ordering = ("-signed_date",)
    search_fields = ("supplier__name",)
    autocomplete_fields = ["supplier"]  # търсене вместо drop-down
    date_hierarchy = "signed_date"

