from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator


phone_validator = RegexValidator(
    regex=r"^\+[1-9]\d{1,14}$",
    message="Въведете валиден телефонен номер, например +359888123456."
)
