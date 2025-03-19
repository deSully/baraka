from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from merchant.models import Merchant


class MerchantActivateView(APIView):
    def post(self, request, *args, **kwargs):
        phone_number = request.data.get("phone_number")
        activation_code = request.data.get("activation_code")

        if not phone_number or not activation_code:
            return Response(
                {"error": "Numéro de téléphone et code d'activation requis."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            merchant = Merchant.objects.get(phone_number=phone_number)
        except Merchant.DoesNotExist:
            return Response(
                {"error": "Marchand non trouvé."}, status=status.HTTP_404_NOT_FOUND
            )

        if merchant.activation_code == activation_code:
            merchant.is_active = True
            merchant.save()
            return Response(
                {"message": "Compte activé avec succès."}, status=status.HTTP_200_OK
            )
        else:
            return Response(
                {"error": "Code d'activation invalide."},
                status=status.HTTP_400_BAD_REQUEST,
            )
