from rest_framework import serializers
from .models import Merchant

class MerchantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Merchant
        fields = ["phone_number", "first_name", "last_name", "is_active"]
