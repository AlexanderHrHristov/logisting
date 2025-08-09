from django.contrib.auth.mixins import UserPassesTestMixin

class GroupRequiredMixin(UserPassesTestMixin):
    allowed_groups = []  # списък с групи, които имат достъп

    def test_func(self):
        user_groups = self.request.user.groups.values_list('name', flat=True)
        return any(group in self.allowed_groups for group in user_groups)


class LegalOnlyMixin(GroupRequiredMixin):
    allowed_groups = ['Legal']


class LogisticsManagerRequiredMixin(GroupRequiredMixin):
    allowed_groups = ['Logistics Manager']


class LogisticsOrManagerRequiredMixin(GroupRequiredMixin):
    allowed_groups = ['Logistics', 'Logistics Manager']


class LogisticsOrLegalRequiredMixin(GroupRequiredMixin):
    allowed_groups = ['Logistics', 'Logistics Manager', 'Legal']
