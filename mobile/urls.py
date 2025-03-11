from mobile.views import *
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

app_name = 'mobile'

urlpatterns = [
    path('categories/', GetCategories.as_view(), name='GetCategories'),
    path('category/<slug:slug>/', CategoryDetails.as_view(), name='CategoryDetails'),
]  + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)