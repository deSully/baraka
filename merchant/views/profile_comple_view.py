from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from merchant.models import Merchant


class MerchantCompleteProfileView(APIView):
    def post(self, request, *args, **kwargs):
        phone_number = request.data.get("phone_number")
        first_name = request.data.get("first_name")
        last_name = request.data.get("last_name")

        if not phone_number or not first_name or not last_name:
            return Response(
                {"error": "Tous les champs sont requis."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            merchant = Merchant.objects.get(phone_number=phone_number)
        except Merchant.DoesNotExist:
            return Response(
                {"error": "Marchand non trouvé."}, status=status.HTTP_404_NOT_FOUND
            )

        merchant.first_name = first_name
        merchant.last_name = last_name
        merchant.save()

        return Response(
            {"message": "Profil mis à jour avec succès."}, status=status.HTTP_200_OK
        )
