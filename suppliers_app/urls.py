from django.urls import path
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
    path('suppliers/', SupplierListView.as_view(), name='supplier-list'),  # списък доставчици
    path('suppliers/add/', SupplierCreateView.as_view(), name='supplier-create'),  # добавяне доставчик
    path('suppliers/edit/<int:pk>/', SupplierUpdateView.as_view(), name='supplier-update'),  # редакция доставчик
    path('suppliers/delete/<int:pk>/', SupplierDeleteView.as_view(), name='supplier-delete'),  # изтриване доставчик
]
