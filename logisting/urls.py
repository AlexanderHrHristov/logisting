from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('core.urls')),        # Home, About, Contact
    # path('users/', include('users.urls')), # Users
    # path('suppliers/', include('suppliers.urls')), # Suppliers
]
