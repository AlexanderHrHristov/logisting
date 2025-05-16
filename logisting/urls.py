from django.contrib import admin
from django.urls import path, include
from users import views as users_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('users.urls')),
    path('', users_views.home_view, name='home'),
    path('about/', users_views.about_view, name='about'),
    path('dashboard/', users_views.dashboard_view, name='dashboard'),  # Всички пътища – включително '/'
]
