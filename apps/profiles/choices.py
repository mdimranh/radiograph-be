from django.db import models


class GenderType(models.TextChoices):
    MALE = "male", "Male"
    FEMALE = "female", "Female"


class MaritalStatusType(models.TextChoices):
    SINGLE = "single", "Single"
    MARRIED = "married", "Married"
    DIVORCED = "divorced", "Divorced"


class BloodGroupType(models.TextChoices):
    A_PLUS = "a+", "A+"
    A_MINUS = "a-", "A-"
    B_PLUS = "b+", "B+"
    B_MINUS = "b-", "B-"
    AB_PLUS = "ab+", "AB+"
    AB_MINUS = "ab-", "AB-"
    O_PLUS = "o+", "O+"
    O_MINUS = "o-", "O-"
