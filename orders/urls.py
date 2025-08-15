from django.urls import path

from . import views

app_name = 'orders'  # това е важно, за да работят namespaced URLs

urlpatterns = [
    path('', views.OrderListView.as_view(), name='list'),      # списък
    path('create/', views.OrderCreateView.as_view(), name='create'),  # създаване
    path('<int:pk>/update/', views.OrderUpdateView.as_view(), name='update'),  # редакция
    path('<int:pk>/delete/', views.OrderDeleteView.as_view(), name='delete'),  # изтриване
]
