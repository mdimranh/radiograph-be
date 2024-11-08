from django.db import models
from utils.models import BaseModel
from utils.fields import PhoneNumberField
from .choices import GenderType, BloodGroupType, MaritalStatusType


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
    certificate = models.FileField(
        "Certificate",
        upload_to="media/certificates",
        null=True,
        blank=True,
    )
    user = models.OneToOneField(
        "account.User",
        on_delete=models.CASCADE,
        related_name="%(class)s_profile",
    )

    class Meta:
        abstract = True

    def __str__(self):
        return f"{self.user.phone}"


class RadiologistProfile(ProfileBase):
    department = models.ForeignKey(
        "account.Department",
        on_delete=models.SET_NULL,
        null=True,
        related_name="radiologist_department",
    )


class RadiographerProfile(ProfileBase):
    department = models.ManyToManyField(
        "account.Department", related_name="radiographer_department"
    )


class AdminProfile(ProfileBase):
    pass
