from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from merchant.models import Merchant

from rest_framework.permissions import AllowAny

class MerchantAuthView(APIView):
    """Vue pour l'authentification d'un marchand"""

    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        # Récupérer le device_id
        device_id = request.data.get('device_id')

        if not device_id:
            return Response({"error": "Device ID est requis."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            merchant = Merchant.objects.get(device_id=device_id)
        except Merchant.DoesNotExist:
            return Response({"error": "Marchand non trouvé."}, status=status.HTTP_404_NOT_FOUND)

        if not merchant.is_active:
            return Response({"error": "Compte non activé."}, status=status.HTTP_400_BAD_REQUEST)

        return Response({"message": "Authentification réussie."}, status=status.HTTP_200_OK)
