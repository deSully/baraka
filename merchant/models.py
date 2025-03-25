from django.contrib.auth.models import AbstractBaseUser
from django.db import models


from django.contrib.auth.models import BaseUserManager


class MerchantManager(BaseUserManager):
    def create_user(self, phone_number, device_id, password=None, **extra_fields):
        if not phone_number:
            raise ValueError("Le numéro de téléphone est obligatoire")
        if not device_id:
            raise ValueError("Le device ID est obligatoire")

        user = self.model(
            phone_number=phone_number, device_id=device_id, **extra_fields
        )
        user.set_password(
            password or device_id
        )  # Le device_id peut être le mot de passe par défaut
        user.save(using=self._db)
        return user

    def create_superuser(self, phone_number, device_id, password=None, **extra_fields):
        extra_fields.setdefault("is_active", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_staff", True)

        return self.create_user(phone_number, device_id, password, **extra_fields)

    def get_by_natural_key(self, phone_number):
        return self.get(phone_number=phone_number)


class Merchant(AbstractBaseUser):
    phone_number = models.CharField(max_length=15, unique=True)
    device_id = models.CharField(max_length=255, unique=True)
    first_name = models.CharField(max_length=255, blank=True, null=True)
    last_name = models.CharField(max_length=255, blank=True, null=True)
    is_active = models.BooleanField(default=False)
    activation_code = models.CharField(max_length=6, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = "phone_number"
    REQUIRED_FIELDS = ["device_id"]

    objects = MerchantManager()

    def __str__(self):
        return f"{self.phone_number} - {self.device_id}"
