from django.contrib import admin
from django.urls import path, include

from users import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('core.urls')),       # Home, About, Contact
    path('register/', views.register, name='register'),
    path('users/', include('users.urls')),

    # path('users/', include('users.urls')), # Users
    # path('suppliers/', include('suppliers.urls')), # Suppliers
]
