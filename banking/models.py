from django.db import models
from django.conf import settings

class ContaEmpresarial(models.Model):
    usuario = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    saldo = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    limite = models.DecimalField(max_digits=15, decimal_places=2, default=0)

    def __str__(self):
        return f"Conta {self.usuario.agencia}/{self.usuario.conta}"

class Movimentacao(models.Model):
    TIPO_CHOICES = [
        ("entrada", "Entrada"),
        ("saida", "Saída"),
    ]
    conta = models.ForeignKey(ContaEmpresarial, on_delete=models.CASCADE, related_name="movimentacoes")
    tipo = models.CharField(max_length=10, choices=TIPO_CHOICES)
    descricao = models.CharField(max_length=200)
    valor = models.DecimalField(max_digits=15, decimal_places=2)
    data = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-data"]

class PixChave(models.Model):
    conta = models.ForeignKey(ContaEmpresarial, on_delete=models.CASCADE)
    chave = models.CharField(max_length=100)
    tipo = models.CharField(max_length=20, choices=[
        ("cnpj", "CNPJ"), ("email", "E-mail"), ("telefone", "Telefone"), ("aleatoria", "Aleatória")
    ])