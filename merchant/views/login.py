from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from merchant.models import Merchant


class MerchantLoginView(APIView):
    def post(self, request, *args, **kwargs):
        phone_number = request.data.get("phone_number")
        device_id = request.data.get("device_id")

        if not phone_number or not device_id:
            return Response(
                {"error": "Numéro de téléphone et device ID requis."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            merchant = Merchant.objects.get(phone_number=phone_number)
        except Merchant.DoesNotExist:
            return Response(
                {"error": "Marchand non trouvé."}, status=status.HTTP_404_NOT_FOUND
            )

        if not merchant.is_active:
            return Response(
                {"error": "Compte non activé."}, status=status.HTTP_400_BAD_REQUEST
            )

        # Vérifier que le `device_id` correspond
        if merchant.device_id != device_id:
            return Response(
                {"error": "Device ID incorrect."}, status=status.HTTP_400_BAD_REQUEST
            )
        
       
        refresh = RefreshToken.for_user(merchant)
        return {
            "refresh": str(refresh),
            "access": str(refresh.access_token),
        }


        # Générer un token d'authentification
        token, _ = Token.objects.get_or_create(user=merchant)

        return Response({"token": token.key}, status=status.HTTP_200_OK)
