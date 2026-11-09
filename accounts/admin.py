from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from unfold.admin import ModelAdmin
from .models import EmpresaUser

@admin.register(EmpresaUser)
class EmpresaUserAdmin(UserAdmin, ModelAdmin):
    list_display = ("username", "razao_social", "cnpj", "cpf_responsavel", "telefone", "agencia", "conta", "is_master")
    fieldsets = UserAdmin.fieldsets + (
        ("Dados Empresariais", {
            "fields": ("cnpj", "cpf_responsavel", "telefone", "razao_social", "agencia", "conta", "is_master")
        }),
    )