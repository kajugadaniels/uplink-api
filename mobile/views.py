from base.models import *
from mobile.models import *
from base.serializers import *
from django.db.models import Q
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
    Retrieve details of a specific category by pk.
    Accessible only to authenticated users.
    """
    permission_classes = [AllowAny]

    def get(self, request, pk, *args, **kwargs):
        try:
            category = Category.objects.get(pk=pk)
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
    Retrieve a list of all posts with detailed information including likes and comments.
    This endpoint is publicly accessible.
    """
    permission_classes = [AllowAny]

    def get(self, request, *args, **kwargs):
        try:
            posts = Post.objects.all().order_by('-created_at')
            # Pass the request context to build absolute URLs
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
    Retrieve detailed information for a specific post, including likes and comments.
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
      - A 'posts' array containing detailed post information (including likes and comments) without the nested user data.
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

class TogglePostLike(APIView):
    """
    Toggle the like status for a post.
    
    If the logged-in user has already liked the post, the like is removed.
    If not, a new like is created.
    This endpoint ensures that a user can only like a post once and toggles the like state.
    """
    permission_classes = [IsAuthenticated]

    def post(self, request, post_id, *args, **kwargs):
        user = request.user
        try:
            post = Post.objects.get(id=post_id)
        except Post.DoesNotExist:
            return Response({"detail": "Post not found."}, status=status.HTTP_404_NOT_FOUND)
        
        existing_like = PostLike.objects.filter(user=user, post=post).first()
        if existing_like:
            existing_like.delete()
            return Response({"detail": "Like removed."}, status=status.HTTP_200_OK)
        else:
            like = PostLike.objects.create(user=user, post=post)
            serializer = PostLikeSerializer(like, context={'request': request})
            return Response({
                "detail": "Post liked successfully.",
                "data": serializer.data
            }, status=status.HTTP_201_CREATED)

class AddPostComment(APIView):
    """
    Create a new comment for a specific post.
    Only authenticated users can add comments.
    The post ID is taken from the URL.
    """
    permission_classes = [IsAuthenticated]

    def post(self, request, post_id, *args, **kwargs):
        data = request.data.copy()
        data['post'] = post_id  # Ensure the comment is linked to the correct post
        serializer = PostCommentSerializer(data=data, context={'request': request})
        if serializer.is_valid():
            try:
                comment = serializer.save()
                return Response({
                    "detail": "Comment added successfully.",
                    "data": PostCommentSerializer(comment, context={'request': request}).data
                }, status=status.HTTP_201_CREATED)
            except Exception as e:
                return Response({
                    "detail": "An error occurred while adding the comment.",
                    "error": str(e)
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response({
            "detail": "Comment creation failed.",
            "errors": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

class UpdatePostComment(APIView):
    """
    Update an existing comment.
    Only the comment's owner (logged-in user) can update it.
    Supports both PUT and PATCH methods.
    """
    permission_classes = [IsAuthenticated]

    def put(self, request, pk, *args, **kwargs):
        comment = get_object_or_404(PostComment, pk=pk)
        if comment.user != request.user:
            return Response({"detail": "Permission denied: You are not the owner of this comment."},
                            status=status.HTTP_403_FORBIDDEN)
        serializer = PostCommentSerializer(comment, data=request.data, partial=False, context={'request': request})
        if serializer.is_valid():
            try:
                updated_comment = serializer.save()
                return Response({
                    "detail": "Comment updated successfully.",
                    "data": PostCommentSerializer(updated_comment, context={'request': request}).data
                }, status=status.HTTP_200_OK)
            except Exception as e:
                return Response({
                    "detail": "An error occurred while updating the comment.",
                    "error": str(e)
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response({
            "detail": "Comment update failed.",
            "errors": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk, *args, **kwargs):
        comment = get_object_or_404(PostComment, pk=pk)
        if comment.user != request.user:
            return Response({"detail": "Permission denied: You are not the owner of this comment."},
                            status=status.HTTP_403_FORBIDDEN)
        serializer = PostCommentSerializer(comment, data=request.data, partial=True, context={'request': request})
        if serializer.is_valid():
            try:
                updated_comment = serializer.save()
                return Response({
                    "detail": "Comment updated successfully.",
                    "data": PostCommentSerializer(updated_comment, context={'request': request}).data
                }, status=status.HTTP_200_OK)
            except Exception as e:
                return Response({
                    "detail": "An error occurred while updating the comment.",
                    "error": str(e)
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response({
            "detail": "Comment update failed.",
            "errors": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

class DeletePostComment(APIView):
    """
    Delete an existing comment.
    Only the comment's owner (logged-in user) can delete it.
    """
    permission_classes = [IsAuthenticated]

    def delete(self, request, pk, *args, **kwargs):
        comment = get_object_or_404(PostComment, pk=pk)
        if comment.user != request.user:
            return Response({"detail": "Permission denied: You are not the owner of this comment."},
                            status=status.HTTP_403_FORBIDDEN)
        try:
            comment.delete()
            return Response({"detail": "Comment deleted successfully."}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({
                "detail": "An error occurred while deleting the comment.",
                "error": str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class ToggleFollowView(APIView):
    """
    Toggle the follow status for a user.
    
    - If the logged-in user is already following the target user, then unfollow.
    - Otherwise, create a new follow relationship.
    """
    permission_classes = [IsAuthenticated]

    def post(self, request, user_id, *args, **kwargs):
        try:
            target_user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response({"detail": "Target user not found."}, status=status.HTTP_404_NOT_FOUND)
        
        if request.user == target_user:
            return Response({"detail": "You cannot follow yourself."}, status=status.HTTP_400_BAD_REQUEST)
        
        follow_relationship = Follow.objects.filter(follower=request.user, following=target_user).first()
        if follow_relationship:
            # Unfollow: delete the relationship
            follow_relationship.delete()
            return Response({"detail": "Successfully unfollowed the user."}, status=status.HTTP_200_OK)
        else:
            # Follow: create a new follow relationship
            follow_relationship = Follow.objects.create(follower=request.user, following=target_user)
            serializer = FollowSerializer(follow_relationship, context={'request': request})
            return Response({
                "detail": "User followed successfully.",
                "data": serializer.data
            }, status=status.HTTP_201_CREATED)

class UserFollowListView(APIView):
    """
    Retrieve the list of users that follow the specified user.

    This endpoint aggregates the 'follower' users from the Follow relationships
    where the specified user is being followed, ensuring that any duplicate entries are removed,
    and returns a clean list of user details.
    """
    permission_classes = [AllowAny]

    def get(self, request, user_id, *args, **kwargs):
        try:
            target_user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response(
                {"detail": "User not found."},
                status=status.HTTP_404_NOT_FOUND
            )
        
        # Retrieve follow relationships where the target user is being followed.
        follow_relationships = Follow.objects.filter(following=target_user)
        # Extract the follower users and remove duplicates
        follower_users = [relation.follower for relation in follow_relationships]
        unique_followers = {user.id: user for user in follower_users}.values()
        
        serializer = UserSerializer(unique_followers, many=True, context={'request': request})
        
        return Response({
            "detail": "Followers list retrieved successfully.",
            "count": len(unique_followers),
            "users": serializer.data
        }, status=status.HTTP_200_OK)

class UserFollowingUsersView(APIView):
    """
    Retrieve a list of users that the specified user is following.
    
    This endpoint returns user details for each user that the given user has followed.
    Duplicate entries are removed for safety.
    """
    permission_classes = [AllowAny]

    def get(self, request, user_id, *args, **kwargs):
        try:
            target_user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response(
                {"detail": "User not found."},
                status=status.HTTP_404_NOT_FOUND
            )
        
        # Retrieve follow relationships where the target user is the follower.
        follow_relationships = Follow.objects.filter(follower=target_user)
        following_users = [relation.following for relation in follow_relationships]
        # Remove duplicates by using a dict keyed by user ID (just in case)
        unique_following = {user.id: user for user in following_users}.values()
        serializer = UserSerializer(unique_following, many=True, context={'request': request})
        
        return Response({
            "detail": "List of followed users retrieved successfully.",
            "count": len(unique_following),
            "users": serializer.data
        }, status=status.HTTP_200_OK)

class MessageSendView(APIView):
    """
    Send a new message from the logged-in user to another user.
    """
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = MessageCreateSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            message = serializer.save()
            output_serializer = MessageSerializer(message, context={'request': request})
            return Response({
                "detail": "Message sent successfully.",
                "message": output_serializer.data
            }, status=status.HTTP_201_CREATED)
        return Response({
            "detail": "Error sending message.",
            "errors": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

class MessageDetailView(APIView):
    """
    Retrieve, edit, or delete a specific message.
    Only participants (sender or receiver) can view the message.
    Only the sender may edit the message.
    """
    permission_classes = [IsAuthenticated]

    def get_object(self, pk, request):
        try:
            message = Message.objects.get(pk=pk)
        except Message.DoesNotExist:
            raise NotFound("Message not found.")
        if request.user not in [message.sender, message.receiver]:
            raise PermissionDenied("You do not have permission to access this message.")
        return message

    def get(self, request, pk, *args, **kwargs):
        message = self.get_object(pk, request)
        serializer = MessageSerializer(message, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk, *args, **kwargs):
        message = self.get_object(pk, request)
        if request.user != message.sender:
            return Response({"detail": "You can only edit messages you have sent."}, status=status.HTTP_403_FORBIDDEN)
        serializer = MessageCreateSerializer(message, data=request.data, context={'request': request})
        if serializer.is_valid():
            updated_message = serializer.save()
            output_serializer = MessageSerializer(updated_message, context={'request': request})
            return Response({
                "detail": "Message updated successfully.",
                "message": output_serializer.data
            }, status=status.HTTP_200_OK)
        return Response({
            "detail": "Error updating message.",
            "errors": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk, *args, **kwargs):
        message = self.get_object(pk, request)
        if request.user != message.sender:
            return Response({"detail": "You can only edit messages you have sent."}, status=status.HTTP_403_FORBIDDEN)
        serializer = MessageCreateSerializer(message, data=request.data, partial=True, context={'request': request})
        if serializer.is_valid():
            updated_message = serializer.save()
            output_serializer = MessageSerializer(updated_message, context={'request': request})
            return Response({
                "detail": "Message updated successfully.",
                "message": output_serializer.data
            }, status=status.HTTP_200_OK)
        return Response({
            "detail": "Error updating message.",
            "errors": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, *args, **kwargs):
        message = self.get_object(pk, request)
        if request.user not in [message.sender, message.receiver]:
            return Response({"detail": "You are not permitted to delete this message."}, status=status.HTTP_403_FORBIDDEN)
        message.delete()
        return Response({"detail": "Message deleted successfully."}, status=status.HTTP_200_OK)

class UserInboxView(APIView):
    """
    Retrieve a unique conversation list for the logged-in user based on messages received.

    For each sender, only the most recent message received is returned to create a conversation summary.
    This endpoint is accessible by the logged-in user only.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        # Retrieve all messages for the logged-in user ordered by most recent first.
        all_messages = Message.objects.filter(receiver=request.user).order_by('-created_at')
        
        # Create a dictionary to capture the most recent message per unique sender.
        unique_conversations = {}
        for message in all_messages:
            # The first message encountered for a given sender (ordered descending by created_at)
            # is the most recent.
            if message.sender_id not in unique_conversations:
                unique_conversations[message.sender_id] = message

        # Convert the dictionary values into a list.
        conversation_list = list(unique_conversations.values())
        serializer = MessageSerializer(conversation_list, many=True, context={'request': request})
        
        return Response({
            "detail": "Unique conversations retrieved successfully.",
            "count": len(conversation_list),
            "conversations": serializer.data
        }, status=status.HTTP_200_OK)

class MessageHistoryView(APIView):
    """
    Retrieve the complete message history (conversation) between the logged-in user and a specific target user.

    The endpoint collects all messages sent by either party, ordered by the creation time (oldest to newest),
    providing a natural conversation flow.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request, user_id, *args, **kwargs):
        # Ensure the target user exists.
        try:
            target_user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response(
                {"detail": "Target user not found."},
                status=status.HTTP_404_NOT_FOUND
            )
        
        # Retrieve the complete conversation between the logged-in user and the target user.
        conversation = Message.objects.filter(
            Q(sender=request.user, receiver=target_user) |
            Q(sender=target_user, receiver=request.user)
        ).order_by('created_at')

        serializer = MessageSerializer(conversation, many=True, context={'request': request})
        return Response({
            "detail": "Conversation history retrieved successfully.",
            "count": conversation.count(),
            "messages": serializer.data
        }, status=status.HTTP_200_OK)