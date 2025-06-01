from django.db import models

class OnSiteDelivery(models.Model):
    date = models.DateField()
    supplier_name = models.CharField(max_length=100)
    time_slot = models.TimeField()
    notes = models.TextField(blank=True)

    def __str__(self):
        return f"{self.date} - {self.supplier_name}"

class PickupDelivery(models.Model):
    date = models.DateField()
    company_name = models.CharField(max_length=100)
    driver_assigned = models.CharField(max_length=100, blank=True)
    notes = models.TextField(blank=True)

    def __str__(self):
        return f"{self.date} - {self.company_name}"

