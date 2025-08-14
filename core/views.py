from django.conf import settings
from django.shortcuts import render
import requests

from core.forms import ContactForm


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


def home_view(request):
    city = "Sofia"
    api_key = settings.OPENWEATHER_API_KEY  # взима ключа от settings.py
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric&lang=bg"

    weather_data = {}
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()  # ще хвърли грешка ако статус код != 200
        data = response.json()

        if "main" in data:
            weather_data = {
                "city": city,
                "temp": round(data["main"]["temp"], 1),  # закръгляме температурата
                "description": data["weather"][0]["description"].capitalize(),
                "humidity": data["main"]["humidity"],
                "icon": f"https://openweathermap.org/img/wn/{data['weather'][0]['icon']}@2x.png"
            }
        else:
            weather_data = {
                "error": data.get("message", "Неуспешно зареждане на времето.")
            }

    except requests.exceptions.RequestException as e:
        weather_data = {
            "error": f"Неуспешно зареждане на времето: {e}"
        }

    return render(request, "core/home.html", {"weather": weather_data})
