from django.contrib.auth import login, authenticate
from django.shortcuts import redirect, render
from .models import EmpresaUser

def login_parte_1(request):
    if request.method == "POST":
        agencia = request.POST.get("agencia")
        conta = request.POST.get("conta")

        # Verifica se existe um usuário com essa agência e conta
        user_exists = EmpresaUser.objects.filter(agencia=agencia, conta=conta).exists()

        if user_exists:
            request.session['agencia'] = agencia
            request.session['conta'] = conta
            return redirect("login_parte_2")
        else:
            return render(request, "accounts/login.html", {"erro": "Agência ou conta não encontrada."})

    return render(request, "accounts/login.html")

def login_parte_2(request):
    agencia = request.session.get('agencia')
    conta = request.session.get('conta')

    # Se o usuário tentar acessar direto sem passar pela etapa 1, volta
    if not agencia or not conta:
        return redirect("login")

    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        # Autentica o usuário
        user = authenticate(request, username=username, password=password)

        if user is not None:
            # Verifica se o usuário autenticado pertence à agência e conta informadas na Etapa 1
            if user.agencia == agencia and user.conta == conta:
                login(request, user)
                return redirect("painel")
            else:
                erro = "Usuário não pertence a esta agência/conta."
        else:
            erro = "Usuário ou senha inválidos."

        return render(request, "accounts/login_parte_2.html", {
            "agencia": agencia,
            "conta": conta,
            "erro": erro
        })

    return render(request, "accounts/login_parte_2.html", {"agencia": agencia, "conta": conta})

def register(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        razao_social = request.POST.get("razao_social", "")
        cnpj = request.POST.get("cnpj", "")
        cpf_responsavel = request.POST.get("cpf", "")
        telefone = request.POST.get("telefone", "")
        if username and password:
            user = EmpresaUser.objects.create_user(
                username=username, password=password,
                razao_social=razao_social, cnpj=cnpj or None,
                cpf_responsavel=cpf_responsavel, telefone=telefone,
            )
            login(request, user)
            return redirect("painel")
    return render(request, "accounts/register.html")

def escolha_conta(request):
    return render(request, "accounts/escolha_conta.html")

def abrir_conta_pj(request):
    if request.method == "POST":
        cpf = request.POST.get("cpf")
        request.session["cpf_temp"] = cpf
        return redirect("register")
    return render(request, "accounts/abrir_conta_pj.html")