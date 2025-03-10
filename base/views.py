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

class AddCategory(APIView):
    """
    Create a new category.
    Accessible only to authenticated users.
    """
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid():
            try:
                category = serializer.save()
                return Response({
                    "detail": "Category created successfully.",
                    "data": CategorySerializer(category).data
                }, status=status.HTTP_201_CREATED)
            except Exception as e:
                return Response({
                    "detail": "An error occurred while creating the category.",
                    "error": str(e)
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response({
            "detail": "Category creation failed.",
            "errors": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

class CategoryDetails(APIView):
    """
    Retrieve details of a specific category by slug.
    Accessible only to authenticated users.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request, slug, *args, **kwargs):
        try:
            category = Category.objects.get(slug=slug)
            serializer = CategorySerializer(category)
            return Response({
                "detail": "Category details retrieved successfully.",
                "data": serializer.data
            }, status=status.HTTP_200_OK)
        except Category.DoesNotExist:
            return Response({
                "detail": "Category not found."
            }, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({
                "detail": "An error occurred while retrieving the category details.",
                "error": str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

