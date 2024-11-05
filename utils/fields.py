from django.core.exceptions import ValidationError
from django.db import models


def validate_phone_number(value):
    # Check if the value is a number and has exactly 11 digits
    if not value.isdigit() or len(value) != 11:
        raise ValidationError("Phone number must be exactly 11 digits.")


class PhoneNumberField(models.CharField):
    def __init__(self, *args, **kwargs):
        # Set max_length to 11 by default if not specified
        kwargs["max_length"] = 11
        super().__init__(*args, **kwargs)

    def clean(self, value, model_instance):
        # Clean method for additional validation
        value = super().clean(value, model_instance)
        validate_phone_number(value)
        return value
