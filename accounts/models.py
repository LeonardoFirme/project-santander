from django.contrib.auth.models import AbstractUser
from django.db import models

class EmpresaUser(AbstractUser):
    cnpj = models.CharField("CNPJ", max_length=18, unique=True, blank=True, null=True)
    cpf_responsavel = models.CharField("CPF do Responsável", max_length=14, blank=True)
    telefone = models.CharField("Telefone", max_length=15, blank=True)
    razao_social = models.CharField("Razão Social", max_length=200, blank=True)
    agencia = models.CharField("Agência", max_length=10, blank=True)
    conta = models.CharField("Conta", max_length=15, blank=True)
    is_master = models.BooleanField("Usuário Master", default=False)

    def __str__(self):
        return self.razao_social or self.username