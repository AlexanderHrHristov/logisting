from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import AppUser

class RegistrationForm(UserCreationForm):
    email = forms.EmailField(
        required=True,
        label='Имейл',
        widget=forms.EmailInput(attrs={
            'placeholder': 'example@stingpharma.com',
            'class': 'form-control',
        }),
        help_text='Задължително поле. Използвайте фирмен имейл с домейн @stingpharma.com.',
    )

    class Meta:
        model = AppUser
        fields = ('username', 'email', 'password1', 'password2')
        widgets = {
            'username': forms.TextInput(attrs={
                'placeholder': 'Потребителско име',
                'class': 'form-control',
            }),
        }
        help_texts = {
            'username': 'Задължително. До 50 символа. Само букви, цифри и @/./+/-/_',
        }

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if not email.endswith('@stingpharma.com'):
            raise forms.ValidationError("Регистрацията е разрешена само с имейл от домейн @stingpharma.com.")
        if AppUser.objects.filter(email=email).exists():
            raise forms.ValidationError("Този имейл вече се използва.")
        return email


class LoginForm(AuthenticationForm):
    username = forms.CharField(
        label='Потребителско име',
        max_length=25,
        widget=forms.TextInput(attrs={
            'placeholder': 'Username',
            'class': 'form-control',
            'autocomplete': 'username',
        }),
    )
    password = forms.CharField(
        label='Парола',
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Password',
            'class': 'form-control',
            'autocomplete': 'current-password',
        }),
    )
    remember_me = forms.BooleanField(
        required=False,
        initial=False,
        label='Запомни ме',
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}),
    )
