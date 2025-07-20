from datetime import date, timedelta
import calendar
from django.shortcuts import render
from .models import ExternalWarehouse
from django.utils.dateparse import parse_date

def external_warehouses_view(request):
    start_date = date.today()
    end_date = start_date + timedelta(days=365)

    dates = []
    current = start_date
    while current <= end_date:
        weekday = current.weekday()  # 0=пон, ..., 6=нед
        if weekday not in (5, 6):  # пропускаме събота (5) и неделя (6)
            day_name = calendar.day_name[weekday]  # на английски: Monday, Tuesday...
            day_name_bg = {
                'Monday': 'Понеделник',
                'Tuesday': 'Вторник',
                'Wednesday': 'Сряда',
                'Thursday': 'Четвъртък',
                'Friday': 'Петък',
            }.get(day_name, '')
            dates.append({
                'date': current.isoformat(),
                'day_name': day_name_bg,
            })
        current += timedelta(days=1)

    selected_date = request.GET.get('date')
    if not selected_date and dates:
        selected_date = dates[0]['date']

    selected_date_obj = parse_date(selected_date)
    records = ExternalWarehouse.objects.filter(date=selected_date_obj) if selected_date_obj else []

    can_add_record = request.user.is_authenticated and (
        getattr(request.user, 'is_logistic', False) or
        getattr(request.user, 'is_logistic_manager', False)
    )

    context = {
        'dates': dates,
        'selected_date': selected_date,
        'records': records,
    }
    return render(request, 'schedules/external_warehouses.html', context)

from django.contrib.auth.decorators import user_passes_test, login_required
from django.shortcuts import redirect
from .forms import ExternalWarehouseForm

def is_logistic_or_manager(user):
    return user.is_authenticated and (user.is_logistic or user.is_logistic_manager)

@login_required
@user_passes_test(is_logistic_or_manager)
def add_external_warehouse_view(request):
    if request.method == 'POST':
        form = ExternalWarehouseForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('external_warehouses')  # промени с името на url-а ти
    else:
        form = ExternalWarehouseForm()

    return render(request, 'schedules/add_external_warehouse.html', {'form': form})
