from django.contrib.auth.models import Group, Permission
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Initialize default user roles'

    def handle(self, *args, **options):
        roles = [
            'Logistics Manager',
            'Logistics',
            'Dealer',
            'Transport Manager',
            'Driver',
            'Warehouseman',
        ]

        for role in roles:
            group, created = Group.objects.get_or_create(name=role)
            if created:
                self.stdout.write(self.style.SUCCESS(f'Created group: {role}'))
            else:
                self.stdout.write(f'Group already exists: {role}')

        self.stdout.write(self.style.SUCCESS('All roles initialized!'))
