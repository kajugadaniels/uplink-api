from base.models import *
from base.serializers import *
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

class GetCategories(APIView):
    """
    Retrieve all categories.
    Accessible only to authenticated users.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        try:
            categories = Category.objects.all().order_by('-id')
            serializer = CategorySerializer(categories, many=True)
            return Response({
                "detail": "Categories retrieved successfully.",
                "data": serializer.data
            }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({
                "detail": "An error occurred while retrieving categories.",
                "error": str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)