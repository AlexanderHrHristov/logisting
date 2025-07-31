from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from .forms import UserRegistrationForm

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False  # 👈 акаунтът е неактивен
            user.save()
            messages.success(request, "Вашата регистрация е приета. След одобрение от администратор ще получите достъп.")
            return redirect('login')
    else:
        form = UserRegistrationForm()
    return render(request, 'users/register.html', {'form': form})
