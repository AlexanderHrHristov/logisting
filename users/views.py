from django.contrib.auth import login as auth_login
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from .forms import LoginForm
from django.http import HttpResponse    
from .forms import RegistrationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages



def home_view(request):
    return HttpResponse("<h1>Добре дошъл в сайта!</h1><p>Това е началната страница.</p>")

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            auth_login(request, user)

            if not form.cleaned_data.get('remember_me'):
                request.session.set_expiry(0)
            else:
                request.session.set_expiry(1209600)

            return redirect('home')
    else:
        form = LoginForm()

    return render(request, 'users/login.html', {'form': form})


def register_view(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False  # 👈 акаунтът е неактивен
            user.save()
            messages.success(request, "Вашата регистрация е приета. След одобрение от администратор ще получите достъп.")
            return redirect('login')
    else:
        form = RegistrationForm()
    return render(request, 'users/register.html', {'form': form})


def home_view(request):
    return render(request, 'users/home.html')


def about_view(request):
    return render(request, 'users/about.html')


@login_required
def dashboard_view(request):
    return render(request, 'users/dashboard.html')

@login_required
def logistics_contacts_view(request):
    # Зареди данните за логистика - примерно от модел или статично
    return render(request, 'users/logistics_contacts.html')

@login_required
def drivers_view(request):
    # Зареди данните за шофьори
    return render(request, 'users/drivers.html')

@login_required
def warehouses_view(request):
    # Зареди данните за складове
    return render(request, 'users/warehouses.html')
