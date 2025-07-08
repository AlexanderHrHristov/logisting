from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from .views import login_view, register_view, home_view
from . import views # Импортираме views от текущото приложение

urlpatterns = [
    path('', home_view, name='home'),  # Начална страница
    path('login/', LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', LogoutView.as_view(next_page='home'), name='logout'),
    path('register/', register_view, name='register'),
    path('about/', views.about_view, name='about'), 
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('logistics_contacts/', views.logistics_contacts_view, name='logistics_contacts'),
    path('drivers/', views.drivers_view, name='drivers'),
    path('warehouses/', views.warehouses_view, name='warehouses'),
    path('dealers/', views.dealers_view, name='dealers'),

]
