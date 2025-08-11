from django.urls import path
from .views import SupplierListView, SupplierCreateView, SupplierUpdateView, SupplierDeleteView, ContractListView, \
    ContractCreateView, ContractUpdateView, ContractToggleActiveView, ContractDeleteView

app_name = 'suppliers'

urlpatterns = [
    path('', SupplierListView.as_view(), name='supplier-list'),
    path('create/', SupplierCreateView.as_view(), name='supplier-create'),
    path('<int:pk>/update/', SupplierUpdateView.as_view(), name='supplier-update'),
    path('<int:pk>/delete/', SupplierDeleteView.as_view(), name='supplier-delete'),
    path('', ContractListView.as_view(), name='contract-list'),
    path('contracts/', ContractListView.as_view(), name='contract-list'),
    path('contracts/create/', ContractCreateView.as_view(), name='contract-create'),
    path('contracts/<int:pk>/update/', ContractUpdateView.as_view(), name='contract-update'),
    path('contracts/<int:pk>/toggle/', ContractToggleActiveView.as_view(), name='contract-toggle'),
    path('contracts/<int:pk>/delete/', ContractDeleteView.as_view(), name='contract-delete'),
]
