from django.contrib.auth.models import BaseUserManager
from django.utils import timezone


class CustomUserManager(BaseUserManager):
    def _create_user(
        self, phone, email, password, is_staff, is_superuser, is_active=True, **kwargs
    ):
        now = timezone.now()

        if not phone:
            raise ValueError("Phone number must be set!")

        if not email:
            raise ValueError("Email must be set!")

        user = self.model(
            username=phone,
            phone=phone,
            email=self.normalize_email(email),
            is_staff=is_staff,
            is_superuser=is_superuser,
            is_active=is_active,
            last_login=now,
            date_joined=now,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, phone, email, password=None, **kwargs):
        return self._create_user(phone, email, password, False, False, **kwargs)

    def create_superuser(self, phone, email, password, **kwargs):
        return self._create_user(phone, email, password, True, True, **kwargs)
