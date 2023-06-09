
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("network.urls")),
]


# Adiciona a configuração para servir arquivos estáticos (CSS, JS, imagens, etc.)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
