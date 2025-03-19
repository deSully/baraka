from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models

class MerchantManager(BaseUserManager):
    def create_user(self, phone_number, device_id, **extra_fields):
        if not phone_number:
            raise ValueError("Le numéro de téléphone est obligatoire")
        if not device_id:
            raise ValueError("Le device ID est obligatoire")
        
        merchant = self.model(phone_number=phone_number, device_id=device_id, **extra_fields)
        merchant.set_password(device_id)  # Le device_id sert de mot de passe
        merchant.save(using=self._db)
        return merchant

class Merchant(AbstractBaseUser):
    phone_number = models.CharField(max_length=15, unique=True)
    device_id = models.CharField(max_length=255, unique=True)
    first_name = models.CharField(max_length=255, blank=True, null=True)
    last_name = models.CharField(max_length=255, blank=True, null=True)
    is_active = models.BooleanField(default=False)
    activation_code = models.CharField(max_length=6, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    objects = MerchantManager()

    USERNAME_FIELD = "phone_number"
    REQUIRED_FIELDS = ["device_id"]

    def __str__(self):
        return f"{self.phone_number} - {self.device_id}"
