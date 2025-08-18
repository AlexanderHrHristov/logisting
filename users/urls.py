from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'users'

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register, name='register'),
    path('password_change/',
         auth_views.PasswordChangeView.as_view(
             template_name='users/password_change.html',
             success_url='/password_change/done/'  # след успешна смяна
         ),
         name='password_change'),
    path('password_change/done/',
         auth_views.PasswordChangeDoneView.as_view(
             template_name='users/password_change_done.html'
         ),
         name='password_change_done'),
]
