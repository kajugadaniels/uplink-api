from base.models import *
from base.serializers import *
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated

class GetCategories(APIView):
    """
    Retrieve all categories.
    Accessible only to authenticated users.
    """
    permission_classes = [AllowAny]

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

class CategoryDetails(APIView):
    """
    Retrieve details of a specific category by slug.
    Accessible only to authenticated users.
    """
    permission_classes = [AllowAny]

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

class GetPosts(APIView):
    """
    Retrieve a list of all posts with detailed information.
    This endpoint is publicly accessible.
    """
    def get(self, request, *args, **kwargs):
        try:
            posts = Post.objects.all().order_by('-created_at')
            serializer = PostSerializer(posts, many=True)
            return Response({
                "detail": "Posts retrieved successfully.",
                "data": serializer.data
            }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({
                "detail": "An error occurred while retrieving posts.",
                "error": str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class AddPost(APIView):
    """
    Create a new post. Only authenticated users can create a post.
    The logged-in user is automatically assigned as the creator of the post.
    """
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        data = request.data.copy()
        data['user'] = request.user.id  # Ensure the post's user is the logged-in user.
        serializer = PostSerializer(data=data)
        if serializer.is_valid():
            try:
                post = serializer.save()
                return Response({
                    "detail": "Post created successfully.",
                    "data": PostSerializer(post).data
                }, status=status.HTTP_201_CREATED)
            except Exception as e:
                return Response({
                    "detail": "An error occurred while creating the post.",
                    "error": str(e)
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response({
            "detail": "Post creation failed.",
            "errors": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)
