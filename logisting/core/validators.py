# core/validators.py

from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from stdnum.eu import vat  # pip install python-stdnum


phone_validator = RegexValidator(
    regex=r"^\+[1-9]\d{1,14}$",
    message="Въведете валиден телефонен номер, например +359888123456."
)


EU_COUNTRY_MAP = {
    "Austria": "AT",
    "Belgium": "BE",
    "Bulgaria": "BG",
    "Croatia": "HR",
    "Cyprus": "CY",
    "Czech Republic": "CZ",
    "Denmark": "DK",
    "Estonia": "EE",
    "Finland": "FI",
    "France": "FR",
    "Germany": "DE",
    "Greece": "GR",
    "Hungary": "HU",
    "Ireland": "IE",
    "Italy": "IT",
    "Latvia": "LV",
    "Lithuania": "LT",
    "Luxembourg": "LU",
    "Malta": "MT",
    "Netherlands": "NL",
    "Poland": "PL",
    "Portugal": "PT",
    "Romania": "RO",
    "Slovakia": "SK",
    "Slovenia": "SI",
    "Spain": "ES",
    "Sweden": "SE",
}


def validate_vat_by_country(vat_number, country_name):
    """
    Validates VAT number based on supplier country.
    For EU countries, uses python-stdnum EU VAT validation.
    For non-EU or unknown countries, applies basic alphanumeric validation.
    """

    if not vat_number:
        return

    clean_vat = vat_number.upper().replace(" ", "")
    country_code = EU_COUNTRY_MAP.get(country_name)

    # Non-EU / unknown country fallback validation
    if not country_code:
        if not clean_vat.isalnum():
            raise ValidationError(
                "VAT номерът трябва да съдържа само цифри и букви."
            )
        return

    # Add country prefix if missing
    if not clean_vat.startswith(country_code):
        check_value = f"{country_code}{clean_vat}"
    else:
        check_value = clean_vat

    if not vat.is_valid(check_value):
        raise ValidationError(
            f"Невалиден VAT номер за държава {country_name}."
        )