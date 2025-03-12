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

class UpdateCategory(APIView):
    """
    Update an existing category.
    Supports both PUT (complete update) and PATCH (partial update).
    Accessible only to authenticated users.
    """
    permission_classes = [IsAuthenticated]

    def put(self, request, slug, *args, **kwargs):
        try:
            category = Category.objects.get(slug=slug)
        except Category.DoesNotExist:
            return Response({
                "detail": "Category not found."
            }, status=status.HTTP_404_NOT_FOUND)

        serializer = CategorySerializer(category, data=request.data, partial=False)
        if serializer.is_valid():
            try:
                serializer.save()
                return Response({
                    "detail": "Category updated successfully.",
                    "data": serializer.data
                }, status=status.HTTP_200_OK)
            except Exception as e:
                return Response({
                    "detail": "An error occurred while updating the category.",
                    "error": str(e)
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response({
            "detail": "Failed to update category.",
            "errors": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, slug, *args, **kwargs):
        try:
            category = Category.objects.get(slug=slug)
        except Category.DoesNotExist:
            return Response({
                "detail": "Category not found."
            }, status=status.HTTP_404_NOT_FOUND)

        serializer = CategorySerializer(category, data=request.data, partial=True)
        if serializer.is_valid():
            try:
                serializer.save()
                return Response({
                    "detail": "Category updated successfully.",
                    "data": serializer.data
                }, status=status.HTTP_200_OK)
            except Exception as e:
                return Response({
                    "detail": "An error occurred while updating the category.",
                    "error": str(e)
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response({
            "detail": "Failed to update category.",
            "errors": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

class DeleteCategory(APIView):
    """
    Delete a category by slug.
    Accessible only to authenticated users.
    """
    permission_classes = [IsAuthenticated]

    def delete(self, request, slug, *args, **kwargs):
        try:
            category = Category.objects.get(slug=slug)
        except Category.DoesNotExist:
            return Response({
                "detail": "Category not found."
            }, status=status.HTTP_404_NOT_FOUND)
        try:
            category.delete()
            return Response({
                "detail": "Category deleted successfully."
            }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({
                "detail": "An error occurred while deleting the category.",
                "error": str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class GetUserPosts(APIView):
    """
    Retrieve a list of posts created by a specific user.
    
    This endpoint is publicly accessible and returns detailed post information
    for the given user (by user ID).
    """
    def get(self, request, user_id, *args, **kwargs):
        try:
            # Retrieve posts for the specified user
            posts = Post.objects.filter(user_id=user_id).order_by('-created_at')
            serializer = PostSerializer(posts, many=True, context={'request': request})
            return Response({
                "detail": "Posts for the user retrieved successfully.",
                "data": serializer.data
            }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({
                "detail": "An error occurred while retrieving posts for the specified user.",
                "error": str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)