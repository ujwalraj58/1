from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
import os

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('chatbot.urls')),
    path('ask/', include('chatbot.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static('/assets/', document_root=os.path.join(settings.BASE_DIR, '../frontend/dist/assets'))
    urlpatterns += static('/', document_root=os.path.join(settings.BASE_DIR, '../frontend/dist'))
