from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from django.conf import settings
from django.conf.urls.static import static
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include("rest_framework.urls")),
    path('', TemplateView.as_view(template_name="index.html")),
    path('api/accounts/', include("accounts.urls")),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pairview'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
] + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)