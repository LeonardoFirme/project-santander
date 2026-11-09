from django.contrib import admin
from django.urls import path, include
from banking.views import painel

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("landing.urls")),
    path("accounts/", include("accounts.urls")),
    path("painel/", painel, name="painel"),
]