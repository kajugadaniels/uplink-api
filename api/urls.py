from django.conf import settings
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static

urlpatterns = [
    path('superadmin/', admin.site.urls),
    path('api/', include('mobile.urls')),
    path('api/admin/', include('base.urls')),
    path('api/auth/', include('account.urls')),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)