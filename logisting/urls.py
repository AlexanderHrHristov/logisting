from django.contrib.auth import views as auth_views
from django.urls import include, path

from logisting.admin_site import custom_admin_site
from users import views

urlpatterns = [
    path('admin/', custom_admin_site.urls),
    path('register/', views.register, name='register'),
    path('users/', include(('users.urls', 'users'), namespace='users')),
    path('suppliers/', include('suppliers.urls', namespace='suppliers')),
    path('orders/', include('orders.urls', namespace='orders')),
    path('login/', auth_views.LoginView.as_view(template_name='users/login.html'), name='login'),
    path('', include('core.urls', namespace='core')),  # Home, About, Contact – винаги накрая
]
