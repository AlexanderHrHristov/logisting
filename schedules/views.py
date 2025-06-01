from datetime import date
from typing import Any

from django.views.generic import TemplateView
from django.utils.timezone import now
from django.shortcuts import render
from .models import OnSiteDelivery, PickupDelivery

class ScheduleView(TemplateView):
    template_name = 'schedules/schedule_view.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        selected_date: date | Any = self.request.GET.get('date') or now().date()
        context['selected_date'] = selected_date
        context['onsite_deliveries'] = OnSiteDelivery.objects.filter(date=selected_date)
        context['pickup_deliveries'] = PickupDelivery.objects.filter(date=selected_date)
        return context
