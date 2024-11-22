from pydoc import describe
from re import U
from tracemalloc import start
from unittest.mock import Base
from django.db import models
from apps import session
from utils.models import BaseModel
from utils.fields import PhoneNumberField
from .choices import GenderType, BloodGroupType, MaritalStatusType
from apps.account.models import User, Department


class Certificate(BaseModel):
    name = models.CharField(max_length=100, unique=True, blank=False)
    start = models.DateField()
    end = models.DateField()
    passedYear = models.PositiveIntegerField()
    result = models.FloatField("Result")
    file = models.FileField("Certificate", upload_to="media/certificates")


class ProfileBase(BaseModel):
    about = models.TextField(max_length=500, blank=True)
    avatar = models.ImageField(
        "Avatar",
        upload_to="media/avatars",
        null=True,
        blank=True,
    )
    gender = models.CharField(
        max_length=20,
        choices=GenderType.choices,
        default=GenderType.MALE,
    )
    marital_status = models.CharField(
        max_length=20,
        choices=MaritalStatusType.choices,
        default=MaritalStatusType.SINGLE,
    )
    blood_group = models.CharField(
        max_length=20,
        choices=BloodGroupType.choices,
        default=BloodGroupType.A_PLUS,
    )
    certificate = models.ManyToManyField(Certificate, blank=True)
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="%(class)s_profile",
    )

    class Meta:
        abstract = True

    def __str__(self):
        return f"{self.user}"


class RadiologistProfile(ProfileBase):
    department = models.ForeignKey(
        Department,
        on_delete=models.SET_NULL,
        null=True,
        related_name="radiologist_department",
    )


class RadiographerProfile(ProfileBase):
    department = models.ForeignKey(
        Department,
        on_delete=models.SET_NULL,
        null=True,
        related_name="radiographer_department",
    )


class AdminProfile(ProfileBase):
    pass
