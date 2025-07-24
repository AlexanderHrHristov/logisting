from django.urls import path
from .views import SupplierListView, SupplierCreateView, SupplierUpdateView, SupplierDeleteView

urlpatterns = [
path('', SupplierListView.as_view(), name='suppliers'),
path('add/', SupplierCreateView.as_view(), name='add_supplier'),
path('<int:pk>/edit/', SupplierUpdateView.as_view(), name='edit_supplier'),
path('<int:pk>/delete/', SupplierDeleteView.as_view(), name='delete_supplier'),
]
