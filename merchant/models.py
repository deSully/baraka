from django.contrib.auth.models import AbstractUser
from django.db import models



class Merchant(AbstractUser):
    phone_number = models.CharField(max_length=15, unique=True, null=True)
    device_id = models.CharField(max_length=255, unique=True, null=True)

    USERNAME_FIELD = "phone_number"
    REQUIRED_FIELDS = ["username", "device_id"]  # username est obligatoire avec AbstractUser

    def __str__(self):
        return f"{self.phone_number} - {self.device_id}"
