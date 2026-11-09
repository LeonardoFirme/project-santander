from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from django.utils import timezone
from .models import ContaEmpresarial

def formatar_brl(valor):
    if valor is None:
        valor = 0
    # Formata com 2 casas decimais, troca ponto por vírgula e adiciona separador de milhar
    return f"{valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

def dashboard_callback(request, context):
    context.update({
        "total_empresas": ContaEmpresarial.objects.count(),
    })
    return context

@login_required
def painel(request):
    conta = ContaEmpresarial.objects.filter(usuario=request.user).first()

    if conta:
        hoje = timezone.now()
        movimentacoes_mes = conta.movimentacoes.filter(data__month=hoje.month, data__year=hoje.year)

        entradas = movimentacoes_mes.filter(tipo='entrada').aggregate(Sum('valor'))['valor__sum'] or 0
        saidas = movimentacoes_mes.filter(tipo='saida').aggregate(Sum('valor'))['valor__sum'] or 0
        balanco = entradas - saidas

        # Formata os valores para o padrão brasileiro
        saldo_fmt = formatar_brl(conta.saldo)
        limite_total_fmt = formatar_brl(conta.saldo + conta.limite)
        entradas_fmt = formatar_brl(entradas)
        saidas_fmt = formatar_brl(saidas)
        balanco_fmt = formatar_brl(abs(balanco))

        # Nome do mês
        meses = ["Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho", "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro"]
        mes_atual = meses[hoje.month - 1]
    else:
        saldo_fmt = "0,00"
        limite_total_fmt = "0,00"
        entradas_fmt = "0,00"
        saidas_fmt = "0,00"
        balanco_fmt = "0,00"
        balanco = 0
        mes_atual = ""

    context = {
        "conta": conta,
        "saldo_fmt": saldo_fmt,
        "limite_total_fmt": limite_total_fmt,
        "entradas_fmt": entradas_fmt,
        "saidas_fmt": saidas_fmt,
        "balanco_fmt": balanco_fmt,
        "balanco_negativo": balanco < 0,
        "mes_atual": mes_atual,
        "data_hoje": timezone.now(),
    }

    return render(request, "banking/dashboard.html", context)