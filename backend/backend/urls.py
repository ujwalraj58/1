# backend/backend/urls.py
from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from django.conf import settings
from django.conf.urls.static import static
import os

urlpatterns = [
    path('admin/', admin.site.urls),
    # Serves the React app's index.html for the root URL
    path('', TemplateView.as_view(template_name='index.html')),

    # IMPORTANT: This line includes the URLs from your 'chatbot' app.
    # The path 'ask/' here means that any URL patterns defined in 'chatbot.urls'
    # will be prefixed with 'ask/'.
    path('ask/', include('chatbot.urls')),
]

# Static file serving for local development (DEBUG=True)
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static('/assets/', document_root=os.path.join(settings.BASE_DIR, '../frontend/dist/assets'))
    urlpatterns += static('/', document_root=os.path.join(settings.BASE_DIR, '../frontend/dist'))

