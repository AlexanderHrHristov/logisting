from django import forms

class ContactForm(forms.Form):
    name = forms.CharField(
        max_length=100,
        label='Име',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Въведи твоето име',
        })
    )
    email = forms.EmailField(
        label='Имейл',
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'example@domain.com',
        })
    )
    message = forms.CharField(
        label='Съобщение',
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'placeholder': 'Твоето съобщение...',
            'rows': 5,
        })
    )
