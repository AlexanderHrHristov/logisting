from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from .views import login_view, register_view, home_view
from . import views # Импортираме views от текущото приложение
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', home_view, name='home'),  # Начална страница
    path('login/', LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('register/', register_view, name='register'),
    path('about/', views.about_view, name='about'),  # 🟢 Добави това
    path('dashboard/', views.dashboard_view, name='dashboard'),
]
