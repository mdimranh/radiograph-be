from django.db import models
from utils.models import BaseModel
from django.contrib.auth.models import AbstractUser
from .user_manager import CustomUserManager
from utils.fields import PhoneNumberField
from .choices import UserStatus, RoleStatus, DepartmentStatus


class Role(BaseModel):
    label = models.CharField(max_length=100, unique=True, blank=False)
    name = models.CharField(max_length=100, unique=True, blank=False)
    salary = models.PositiveIntegerField(default=0)
    status = models.CharField(
        max_length=20,
        choices=RoleStatus.choices,
        default=RoleStatus.ACTIVE,
    )

    def users(self):
        return self.users.all()[:5]

    def __str__(self):
        return f"{self.name} ({self.label})"


class Department(BaseModel):
    label = models.CharField(max_length=100, unique=True, blank=False)
    name = models.CharField(max_length=100, unique=True, blank=False)
    cost = models.PositiveIntegerField(default=0)
    status = models.CharField(
        max_length=20,
        choices=DepartmentStatus.choices,
        default=DepartmentStatus.ACTIVE,
    )

    def __str__(self):
        return f"{self.name} ({self.label})"


class User(AbstractUser, BaseModel):
    phone = PhoneNumberField(unique=True, db_index=True, verbose_name="Phone Number")
    email = models.EmailField(unique=True, db_index=True, max_length=50)
    avatar = models.ImageField(
        "Avatar",
        upload_to="avatars",
        null=True,
        blank=True,
    )
    role = models.ForeignKey(
        Role, related_name="users", on_delete=models.SET_NULL, null=True, blank=True
    )
    status = models.CharField(
        max_length=20,
        choices=UserStatus.choices,
        default=UserStatus.ACTIVE,
    )
    objects = CustomUserManager()

    USERNAME_FIELD = "phone"
    REQUIRED_FIELDS = ["email"]
    USERNAME_FIELD = "phone"


class Rediologist(BaseModel):
    phone = PhoneNumberField(unique=True, db_index=True, verbose_name="Phone Number")
    email = models.EmailField(unique=True, db_index=True, max_length=50)
    avatar = models.ImageField(
        "Avatar",
        upload_to="avatars",
        null=True,
        blank=True,
    )
    status = models.CharField(
        max_length=20,
        choices=UserStatus.choices,
        default=UserStatus.ACTIVE,
    )
    department = models.ManyToManyField(
        Department, related_name="rediologists", blank=True
    )

    def __str__(self):
        return f"{self.phone}"
