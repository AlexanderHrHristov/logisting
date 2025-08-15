from django.contrib import messages
from django.contrib.auth.mixins import UserPassesTestMixin
from django.shortcuts import redirect


class GroupRequiredMixin(UserPassesTestMixin):
    allowed_groups = []  # списък с групи, които имат достъп
    permission_message = "Нямате права за тази операция."  # по подразбиране

    def test_func(self):
        user = self.request.user
        if user.is_superuser:
            return True
        return user.groups.filter(name__in=self.allowed_groups).exists()

    def handle_no_permission(self):
        messages.error(self.request, getattr(self, 'permission_message', self.permission_message))
        return redirect('orders:list')


class LegalOnlyMixin(GroupRequiredMixin):
    allowed_groups = ['Legal']

    
class LogisticsManagerRequiredMixin(GroupRequiredMixin):
    allowed_groups = ['Logistics Manager']

   

class LogisticsOrManagerRequiredMixin(GroupRequiredMixin):
    allowed_groups = ['Logistics', 'Logistics Manager']


class LogisticsOrLegalRequiredMixin(GroupRequiredMixin):
    allowed_groups = ['Logistics', 'Logistics Manager', 'Legal']

    