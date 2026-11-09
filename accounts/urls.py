from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path("login/", views.login_parte_1, name="login"),
    path("login/usuario/", views.login_parte_2, name="login_parte_2"),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
    path("register/", views.register, name="register"),
    path("abrir-conta/", views.escolha_conta, name="escolha_conta"),
    path("abrir-conta-pj/", views.abrir_conta_pj, name="abrir_conta_pj"),
]