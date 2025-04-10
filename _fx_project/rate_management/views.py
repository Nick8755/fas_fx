from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import Rate
from .serializers import RateReadSerializer, RateWriteSerializer

class RateListCreateView(APIView): #View to getting all rates
    def get(self, request):
        rates = Rate.objects.select_related(
            'currency_pair',
            'currency_pair__base_currency',
            'currency_pair__quote_currency',
            'provider'
        ).prefetch_related(
            'currency_pair__supported_providers'
        )

        serializer = RateReadSerializer(rates, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = RateWriteSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


