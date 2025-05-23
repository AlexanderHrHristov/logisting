# Generated by Django 5.2.1 on 2025-05-19 08:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_appuser_is_dealer'),
    ]

    operations = [
        migrations.AddField(
            model_name='appuser',
            name='created_by_admin',
            field=models.BooleanField(default=False, verbose_name='Създаден от админ'),
        ),
        migrations.AddField(
            model_name='appuser',
            name='notes',
            field=models.TextField(blank=True, null=True, verbose_name='Бележки'),
        ),
        migrations.AddField(
            model_name='appuser',
            name='phone',
            field=models.CharField(blank=True, max_length=20, null=True, verbose_name='Телефон'),
        ),
        migrations.AddField(
            model_name='appuser',
            name='position',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='Длъжност'),
        ),
    ]
