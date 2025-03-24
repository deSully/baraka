from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from merchant.models import Merchant
import random
import string

from rest_framework.permissions import AllowAny


class MerchantRegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        phone_number = request.data.get("phone_number")
        device_id = request.data.get("device_id")

        if not phone_number or not device_id:
            return Response(
                {"error": "Numéro de téléphone et device ID requis."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        merchant, _ = Merchant.objects.get_or_create(
            phone_number=phone_number, defaults={"device_id": device_id}
        )

        # Générer un code d'activation
        activation_code = "".join(random.choices(string.digits, k=6))
        merchant.activation_code = activation_code
        merchant.save()

        # Envoyer le code (WhatsApp, SMS, etc.)
        self.send_code_via_whatsapp(phone_number, activation_code)

        return Response(
            {"message": "Code d'activation envoyé."}, status=status.HTTP_201_CREATED
        )

    def send_code_via_whatsapp(self, phone_number, code):
        pass  # Implémentation de l'envoi ici
