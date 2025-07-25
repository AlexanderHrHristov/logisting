from django.urls import path
from . import views
from .views import (
    external_warehouses_view,
    add_external_warehouse_view,
    SupplierListView,
    SupplierCreateView,
    SupplierUpdateView,
    SupplierDeleteView,
)

urlpatterns = [
    # External Warehouses
    path('external-warehouses/', external_warehouses_view, name='external_warehouses'),
    path('external-warehouses/add/', add_external_warehouse_view, name='add_external_warehouse'),

    # Suppliers
    path('suppliers/', SupplierListView.as_view(), name='supplier-list'),
    path('suppliers/add/', SupplierCreateView.as_view(), name='supplier-create'),
    path('suppliers/<int:pk>/edit/', SupplierUpdateView.as_view(), name='supplier-update'),
    path('suppliers/<int:pk>/delete/', SupplierDeleteView.as_view(), name='supplier-delete'),
]