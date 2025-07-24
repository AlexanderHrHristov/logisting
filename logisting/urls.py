from django.contrib import admin
from django.urls import path, include

from suppliers_app import urls

from suppliers_app.views import supplier_list
from django.contrib.auth.decorators import login_required


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('users.urls')),  # Всичко се управлява от users.urls
    # path('suppliers/', include('suppliers_app.urls')),
    path('suppliers/', supplier_list, name='suppliers'),
]