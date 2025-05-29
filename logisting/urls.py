from django.contrib import admin
from django.urls import path, include



urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('users.urls')),  # Всичко се управлява от users.urls
]