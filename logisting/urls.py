from django.contrib import admin
from django.urls import path, include

from schedules import urls

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('users.urls')),  # Всичко се управлява от users.urls
    path('schedule/', include('schedules.urls')),
]