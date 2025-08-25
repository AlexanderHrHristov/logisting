# suppliers/urls.py
from django.urls import path

from . import views
from .views import (
    SupplierListView, SupplierCreateView, SupplierUpdateView, SupplierDeleteView,
    ContractListView, ContractCreateView, ContractUpdateView, ContractDeleteView, ContractToggleActiveView,
    DeliveryScheduleListView, DeliveryScheduleCreateView, DeliveryScheduleUpdateView,
)


app_name = 'suppliers'



urlpatterns = [
    # --- Доставчици ---
    path('', SupplierListView.as_view(), name='supplier-list'),
    path('create/', SupplierCreateView.as_view(), name='supplier-create'),
    path('<int:pk>/update/', SupplierUpdateView.as_view(), name='supplier-update'),
    path('<int:pk>/delete/', SupplierDeleteView.as_view(), name='supplier-delete'),

    # --- Договори ---
    path('contracts/', ContractListView.as_view(), name='contract-list'),
    path('contracts/create/', ContractCreateView.as_view(), name='contract-create'),
    path('contracts/<int:pk>/update/', ContractUpdateView.as_view(), name='contract-update'),
    path('contracts/<int:pk>/toggle/', ContractToggleActiveView.as_view(), name='contract-toggle'),
    path('contracts/<int:pk>/delete/', ContractDeleteView.as_view(), name='contract-delete'),
    path('contracts/<str:filename>/', views.serve_contract, name='serve_contract'),

    # --- График на доставки ---
    path('delivery-schedule/', DeliveryScheduleListView.as_view(), name='delivery_schedule_list'),
    path('delivery-schedule/add/', DeliveryScheduleCreateView.as_view(), name='delivery_schedule_create'),
    path('delivery-schedule/<int:pk>/edit/', DeliveryScheduleUpdateView.as_view(), name='delivery_schedule_update'),

    # --- График за вземане ---
    path("pickup-schedule/", views.PickupScheduleListView.as_view(), name="pickup_schedule_list"),
    path("pickup-schedule/add/", views.PickupScheduleCreateView.as_view(), name="pickup_create"),
    path("pickup-schedule/<int:pk>/edit/", views.PickupScheduleUpdateView.as_view(), name="pickup_schedule_edit"),
    path("pickup-schedule/<int:pk>/delete/", views.PickupScheduleDeleteView.as_view(), name="pickup_delete"),
]

