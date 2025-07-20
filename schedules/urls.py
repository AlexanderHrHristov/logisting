from django.urls import path
from . import views

urlpatterns = [
    path('external-warehouses/', views.external_warehouses_view, name='external_warehouses'),
    path('external-warehouses/add/', views.add_external_warehouse_view, name='add_external_warehouse'),
]
