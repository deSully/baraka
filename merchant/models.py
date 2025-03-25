from django.contrib.auth.models import AbstractBaseUser
from django.db import models



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

    def __str__(self):
        return f"{self.phone_number} - {self.device_id}"
