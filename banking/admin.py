from django.contrib import admin
from django.db.models import Sum
from django.utils import timezone
from unfold.admin import ModelAdmin
from unfold.decorators import display
from .models import ContaEmpresarial, Movimentacao, PixChave


@admin.register(ContaEmpresarial)
class ContaAdmin(ModelAdmin):
    list_display = ("usuario", "saldo_formatado", "limite_formatado")
    search_fields = ("usuario__razao_social", "usuario__cnpj")

    @display(description="Saldo")
    def saldo_formatado(self, obj):
        return f"R$ {obj.saldo:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

    @display(description="Limite")
    def limite_formatado(self, obj):
        return f"R$ {obj.limite:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")


@admin.register(Movimentacao)
class MovimentacaoAdmin(ModelAdmin):
    list_display = ("conta", "tipo_badge", "descricao", "valor_formatado", "data")
    list_filter = ("tipo", "data")
    search_fields = ("descricao", "conta__usuario__razao_social")
    date_hierarchy = "data"

    # Exibe as movimentações mais recentes primeiro
    ordering = ("-data",)

    @display(description="Tipo")
    def tipo_badge(self, obj):
        if obj.tipo == "entrada":
            return "Entrada"
        return "Saída"

    @display(description="Valor")
    def valor_formatado(self, obj):
        return f"R$ {obj.valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

    # --- Cálculo do Fluxo no Topo do Admin ---
    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}

        # Calcula os totais do mês atual
        hoje = timezone.now()
        movs_mes = Movimentacao.objects.filter(data__month=hoje.month, data__year=hoje.year)

        entradas = movs_mes.filter(tipo='entrada').aggregate(Sum('valor'))['valor__sum'] or 0
        saidas = movs_mes.filter(tipo='saida').aggregate(Sum('valor'))['valor__sum'] or 0
        balanco = entradas - saidas

        # Formata os valores em BRL
        def brl(v):
            return f"{v:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

        extra_context['fluxo_entradas'] = brl(entradas)
        extra_context['fluxo_saidas'] = brl(saidas)
        extra_context['fluxo_balanco'] = brl(abs(balanco))
        extra_context['fluxo_balanco_negativo'] = balanco < 0
        extra_context['fluxo_mes'] = hoje.strftime("%B").capitalize()

        return super().changelist_view(request, extra_context=extra_context)


@admin.register(PixChave)
class PixAdmin(ModelAdmin):
    list_display = ("conta", "chave", "tipo")
    search_fields = ("chave", "conta__usuario__razao_social")