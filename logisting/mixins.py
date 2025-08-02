from django.contrib.auth.mixins import UserPassesTestMixin

class LogisticsManagerRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.groups.filter(name='Logistics Manager').exists()

class LogisticsOrManagerRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.groups.filter(name__in=['Logistics', 'Logistics Manager']).exists()

