from django.conf import settings
from django.db import models
from django.utils import timezone
from core.validators import phone_validator


class Supplier(models.Model):
    class DeliveryMethod(models.TextChoices):
        DELIVERY = "delivery", "Доставка на място"
        PICKUP = "pickup", "Вземане от външен склад"

    company_name = models.CharField(
        max_length=255,
        unique=True,
        verbose_name="Доставчик",
    )

    vat_number = models.CharField(
        max_length=30,
        unique=True,
        blank=True,
        null=True,
        verbose_name="ДДС номер",
    )

    email = models.EmailField(
        max_length=255,
        blank=True,
        verbose_name="Имейл",
    )

    phone = models.CharField(
        max_length=20,
        blank=True,
        validators=[phone_validator],
        help_text="Format: +359XXXXXXXXX",
        verbose_name="Телефон",
    )

    contact_person = models.CharField(
        max_length=255,
        blank=True,
        verbose_name="Лице за контакт",
    )

    delivery_method = models.CharField(
        max_length=20,
        choices=DeliveryMethod.choices,
        default=DeliveryMethod.DELIVERY,
        verbose_name="Тип доставка",
    )

    responsible_logistician = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="responsible_suppliers",
        verbose_name="Отговорен логистик",
    )

    is_active = models.BooleanField(
        default=True,
        verbose_name="Активен",
    )

    notes = models.TextField(
        blank=True,
        verbose_name="Бележки",
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["company_name"]
        verbose_name = "Доставчик"
        verbose_name_plural = "Доставчици"

    def __str__(self):
        return self.company_name

    def clean(self):
        super().clean()

        # нормализация на телефон
        if self.phone and not self.phone.startswith("+"):
            self.phone = "+359" + self.phone.lstrip("0")

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

class SupplierContract(models.Model):
    class ContractType(models.TextChoices):
        SUPPLY = "supply", "Доставка на стоки"
        SERVICE = "service", "Услуги"
        OTHER = "other", "Друго"

    supplier = models.ForeignKey(
        Supplier,
        on_delete=models.CASCADE,
        related_name="contracts",
        verbose_name="Доставчик",
    )

    contract_type = models.CharField(
        max_length=20,
        choices=ContractType.choices,
        default=ContractType.SUPPLY,
        verbose_name="Тип договор",
    )

    document_type = models.CharField(
        max_length=100,
        blank=True,
        verbose_name="Тип документ",
        help_text="Напр. договор, анекс, рамково споразумение",
    )

    contract_number = models.CharField(
        max_length=100,
        blank=True,
        verbose_name="Номер на договор",
    )

    signed_date = models.DateField(
        verbose_name="Дата на подписване",
    )

    expiry_date = models.DateField(
        null=True,
        blank=True,
        verbose_name="Дата на изтичане",
    )

    file = models.FileField(
        upload_to="contracts/",
        blank=True,
        null=True,
        verbose_name="Файл",
    )

    is_active = models.BooleanField(
        default=True,
        verbose_name="Активен",
    )

    notes = models.TextField(
        blank=True,
        verbose_name="Бележки",
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def is_expired(self):
        return bool(self.expiry_date and self.expiry_date < timezone.now().date())

    @property
    def is_currently_active(self):
        return self.is_active and not self.is_expired

    class Meta:
        ordering = ["-signed_date", "supplier"]
        verbose_name = "Договор"
        verbose_name_plural = "Договори"

    def __str__(self):
        return f"{self.get_contract_type_display()} – {self.supplier.company_name}"