from django.db import models
from django.contrib.auth.models import User

class ExternalWarehouse(models.Model):
    date = models.DateField()  # дата на запис
    supplier = models.CharField("Доставчик", max_length=30)
    location = models.CharField("Локация", max_length=30)
    volume = models.DecimalField("Обем", max_digits=3, decimal_places=1)
    thermolabile = models.BooleanField("Термолабилни")
    narcotic = models.BooleanField("Наркотични")
    note = models.TextField("Забележка", blank=True, null=True)
    driver = models.CharField("Към Транспорт", max_length=100)
    received = models.BooleanField("Получено", default=False)

    def __str__(self):
        return f"{self.date} - {self.supplier} - {self.location}"
