from mobile.views import *
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

app_name = 'mobile'

urlpatterns = [
    path('categories/', GetCategories.as_view(), name='GetCategories'),
    path('category/<int:pk>/', CategoryDetails.as_view(), name='CategoryDetails'),

    path('posts/', GetPosts.as_view(), name='GetPosts'),
    path('post/add/', AddPost.as_view(), name='AddPost'),
    path('post/<int:pk>/', PostDetails.as_view(), name='PostDetails'),
    path('post/<int:pk>/update/', UpdatePost.as_view(), name='UpdatePost'),
    path('post/<int:pk>/delete/', DeletePost.as_view(), name='DeletePost'),
    path('posts/user/<int:user_id>/', GetUserPosts.as_view(), name='GetUserPosts'),

    path('post/<int:post_id>/like/', TogglePostLike.as_view(), name='TogglePostLike'),

    path('post/<int:post_id>/comment/add/', AddPostComment.as_view(), name='AddPostComment'),
    path('post/comment/<int:pk>/update/', UpdatePostComment.as_view(), name='UpdatePostComment'),
    path('post/comment/<int:pk>/delete/', DeletePostComment.as_view(), name='DeletePostComment'),

    path('user/<int:user_id>/toggle-follow/', ToggleFollowView.as_view(), name='ToggleFollow'),
    path('user/<int:user_id>/followers/', UserFollowListView.as_view(), name='UserFollowList'),
    path('user/<int:user_id>/following/', UserFollowingUsersView.as_view(), name='UserFollowingUsers'),

    path('message/send/', MessageSendView.as_view(), name='MessageSend'),
    path('message/<int:pk>/', MessageDetailView.as_view(), name='MessageDetail'),
    path('user/<int:user_id>/inbox/', UserInboxView.as_view(), name='UserInbox'),
    path('message/history/<int:user_id>/', MessageHistoryView.as_view(), name='MessageHistory'),
]  + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)