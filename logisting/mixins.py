from django.contrib.auth.mixins import UserPassesTestMixin

class GroupRequiredMixin(UserPassesTestMixin):
    allowed_groups = []  # списък с групи, които имат достъп

    def test_func(self):
        user = self.request.user
        if user.is_superuser:
            return True
        return user.groups.filter(name__in=self.allowed_groups).exists()


class LegalOnlyMixin(GroupRequiredMixin):
    allowed_groups = ['Legal']


class LogisticsManagerRequiredMixin(GroupRequiredMixin):
    allowed_groups = ['Logistics Manager']


class LogisticsOrManagerRequiredMixin(GroupRequiredMixin):
    allowed_groups = ['Logistics', 'Logistics Manager']


class LogisticsOrLegalRequiredMixin(GroupRequiredMixin):
    allowed_groups = ['Logistics', 'Logistics Manager', 'Legal']


