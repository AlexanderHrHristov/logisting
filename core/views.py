from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.contrib import messages
from .forms import ContactForm


def home(request):
    return render(request, 'home.html')

def about(request):
    return render(request, 'about.html')


def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            message = form.cleaned_data['message']

            subject = f"Новo съобщение от {name}"
            full_message = f"От: {name} <{email}>\n\n{message}"
            from_email = 'ahri.devbox@gmail.com'  # Твоят имейл
            to_email = ['ahri.devbox@gmail.com']   # Къде да се праща

            try:
                send_mail(subject, full_message, from_email, to_email, fail_silently=False)
                messages.success(request, 'Съобщението беше изпратено успешно!')
                return redirect('contact')
            except Exception as e:
                messages.error(request, f'Грешка при изпращане на съобщението: {e}')
        else:
            messages.error(request, 'Моля, поправете грешките във формата.')
    else:
        form = ContactForm()

    return render(request, 'contact.html', {'form': form})

