from mobile.views import *
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

app_name = 'mobile'

urlpatterns = [
    path('categories/', GetCategories.as_view(), name='GetCategories'),
    path('category/<slug:slug>/', CategoryDetails.as_view(), name='CategoryDetails'),

    path('posts/', GetPosts.as_view(), name='GetPosts'),
    path('post/add/', AddPost.as_view(), name='AddPost'),
    path('post/<int:pk>/', PostDetails.as_view(), name='PostDetails'),
    path('post/<int:pk>/update/', UpdatePost.as_view(), name='UpdatePost'),
    path('post/<int:pk>/delete/', DeletePost.as_view(), name='DeletePost'),
    path('posts/user/<int:user_id>/', GetUserPosts.as_view(), name='GetUserPosts'),
    path('post/<int:post_id>/like/', TogglePostLike.as_view(), name='TogglePostLike'),
]  + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)