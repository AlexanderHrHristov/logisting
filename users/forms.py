from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model

import re

User = get_user_model()

class UserRegistrationForm(UserCreationForm):
    username = forms.CharField(
        label="Потребителско име",
        max_length=20,
        help_text="До 20 символа. Разрешени са букви, цифри и точка (.)",
        widget=forms.TextInput(attrs={'class': 'form-control'}),
    )

    password1 = forms.CharField(
        label="Парола",
        strip=False,
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        help_text=(
            "Паролата трябва да е поне 8 символа.<br>"
            "Да не съвпада с лична информация.<br>"
            "Да не е твърде проста или популярна.<br>"
            "Да не е изцяло числова."
        ),
    )

    password2 = forms.CharField(
        label="Потвърди паролата",
        strip=False,
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        help_text="Въведете същата парола отново за потвърждение.",
    )

    email = forms.EmailField(label="Имейл", widget=forms.EmailInput(attrs={'class': 'form-control'}))
    first_name = forms.CharField(label="Име", widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_name = forms.CharField(label="Фамилия", widget=forms.TextInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'password1', 'password2']

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if not re.match(r'^[A-Za-z0-9.]+$', username):
            raise forms.ValidationError("Разрешени са само букви, цифри и точка (.)")
        return username


