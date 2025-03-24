from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from merchant.serializers import MerchantSerializer


class MerchantDetailView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Récupérer les détails du Merchant connecté",
        manual_parameters=[
            openapi.Parameter(
                "Authorization",
                openapi.IN_HEADER,
                description="Token JWT (format: Bearer <token>)",
                type=openapi.TYPE_STRING,
                required=True,
            )
        ],
        responses={200: MerchantSerializer()},
    )
    def get(self, request):
        merchant = request.user
        serializer = MerchantSerializer(merchant)
        return Response(serializer.data)
