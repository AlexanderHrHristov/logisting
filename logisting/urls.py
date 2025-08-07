from django.urls import path, include
from django.contrib import admin
from users import views
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('register/', views.register, name='register'),
    path('', include('core.urls', namespace='core')),    # Home, About, Contact
    path('users/', include(('users.urls', 'users'), namespace='users')),
    path('suppliers/', include('suppliers.urls')),
    path('login/', auth_views.LoginView.as_view(template_name='users/login.html'), name='login')

]
