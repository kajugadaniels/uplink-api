from base.views import *
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

app_name = 'base'

urlpatterns = [
    path('categories/', GetCategories.as_view(), name='GetCategories'),
    path('category/add/', AddCategory.as_view(), name='AddCategory'),
    path('category/<slug:slug>/', CategoryDetails.as_view(), name='CategoryDetails'),
    path('category/<slug:slug>/update/', UpdateCategory.as_view(), name='UpdateCategory'),
    path('category/<slug:slug>/delete/', DeleteCategory.as_view(), name='DeleteCategory'),
]  + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)