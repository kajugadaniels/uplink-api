from base.models import *
from mobile.models import *
from base.serializers import *
from mobile.serializers import *
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
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
    permission_classes = [AllowAny]

    def get(self, request, *args, **kwargs):
        try:
            posts = Post.objects.all().order_by('-created_at')
            # Pass the request in the context to build absolute URLs
            serializer = PostSerializer(posts, many=True, context={'request': request})
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
        serializer = PostSerializer(data=data, context={'request': request})
        if serializer.is_valid():
            try:
                post = serializer.save()
                return Response({
                    "detail": "Post created successfully.",
                    "data": PostSerializer(post, context={'request': request}).data
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

class PostDetails(APIView):
    """
    Retrieve detailed information for a specific post.
    This endpoint is publicly accessible.
    """
    permission_classes = [AllowAny]

    def get(self, request, pk, *args, **kwargs):
        try:
            post = get_object_or_404(Post, pk=pk)
            # Pass the request context to build absolute URLs in nested serializers
            serializer = PostSerializer(post, context={'request': request})
            return Response({
                "detail": "Post details retrieved successfully.",
                "data": serializer.data
            }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({
                "detail": "An error occurred while retrieving post details.",
                "error": str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class UpdatePost(APIView):
    """
    Update an existing post. Only the creator (logged-in user) of the post can update it.
    The updated_at field is automatically updated on save.
    Supports both full (PUT) and partial (PATCH) updates.
    """
    permission_classes = [IsAuthenticated]

    def put(self, request, pk, *args, **kwargs):
        post = get_object_or_404(Post, pk=pk)
        if post.user != request.user:
            return Response({
                "detail": "Permission denied: You are not the owner of this post."
            }, status=status.HTTP_403_FORBIDDEN)
        serializer = PostSerializer(post, data=request.data, partial=False)
        if serializer.is_valid():
            try:
                updated_post = serializer.save()  # updated_at is auto-triggered here.
                return Response({
                    "detail": "Post updated successfully.",
                    "data": PostSerializer(updated_post).data
                }, status=status.HTTP_200_OK)
            except Exception as e:
                return Response({
                    "detail": "An error occurred while updating the post.",
                    "error": str(e)
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response({
            "detail": "Post update failed.",
            "errors": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk, *args, **kwargs):
        post = get_object_or_404(Post, pk=pk)
        if post.user != request.user:
            return Response({
                "detail": "Permission denied: You are not the owner of this post."
            }, status=status.HTTP_403_FORBIDDEN)
        serializer = PostSerializer(post, data=request.data, partial=True)
        if serializer.is_valid():
            try:
                updated_post = serializer.save()  # updated_at is auto-triggered here.
                return Response({
                    "detail": "Post updated successfully.",
                    "data": PostSerializer(updated_post).data
                }, status=status.HTTP_200_OK)
            except Exception as e:
                return Response({
                    "detail": "An error occurred while updating the post.",
                    "error": str(e)
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response({
            "detail": "Post update failed.",
            "errors": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

class DeletePost(APIView):
    """
    Delete an existing post. Only the creator (logged-in user) of the post can delete it.
    """
    permission_classes = [IsAuthenticated]

    def delete(self, request, pk, *args, **kwargs):
        post = get_object_or_404(Post, pk=pk)
        if post.user != request.user:
            return Response({
                "detail": "Permission denied: You are not the owner of this post."
            }, status=status.HTTP_403_FORBIDDEN)
        try:
            post.delete()
            return Response({
                "detail": "Post deleted successfully."
            }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({
                "detail": "An error occurred while deleting the post.",
                "error": str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class GetUserPosts(APIView):
    """
    Retrieve a list of posts created by a specific user, with user information returned only once.
    
    This endpoint is publicly accessible and returns:
      - A top-level 'user' object containing detailed user info.
      - A 'posts' array containing detailed post information without the nested user data.
    """
    permission_classes = [AllowAny]

    def get(self, request, user_id, *args, **kwargs):
        try:
            posts = Post.objects.filter(user_id=user_id).order_by('-created_at')
            User = get_user_model()
            if posts.exists():
                user = posts.first().user
            else:
                user = get_object_or_404(User, pk=user_id)
            serializer = PostSerializer(posts, many=True, context={'request': request})
            serialized_posts = serializer.data
            # Remove the redundant 'user' key from each post object
            for post in serialized_posts:
                post.pop('user', None)
            return Response({
                "detail": "Posts for the user retrieved successfully.",
                "user": UserSerializer(user, context={'request': request}).data,
                "posts": serialized_posts
            }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({
                "detail": "An error occurred while retrieving posts for the specified user.",
                "error": str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)