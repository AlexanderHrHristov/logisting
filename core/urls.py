from django.urls import path, include
from . import views

app_name = 'core'  # <---- Това регистрира namespace 'core'

urlpatterns = [
    path('', views.home_view, name='home'),
    path('about/', views.about_view, name='about'),
    path('contact/', views.contact_view, name='contact'),
    path('accounts/', include('django.contrib.auth.urls')),  # <--- Добави това!
]
