from django.contrib import admin
from django.urls import path, include

from suppliers_app import urls

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('users.urls')),  # Всичко се управлява от users.urls
    path('suppliers/', include('suppliers_app.urls')),
]