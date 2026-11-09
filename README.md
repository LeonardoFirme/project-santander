# Santander Empresas — Painel Administrativo (Projeto Didático)

> ⚠️ **AVISO IMPORTANTE:** Este é um **projeto estritamente didático e acadêmico**, desenvolvido para fins de estudo de Django, Tailwind CSS e replicação de interfaces. **Não possui qualquer vínculo com o Banco Santander S.A.**, não é um produto oficial, não processa dados reais e **não deve ser utilizado em produção**. Todas as marcas, logotipos e referências visuais pertencem aos seus respectivos proprietários e são usadas aqui apenas como referência de estudo.

---

## 📸 Preview

![Preview do projeto](template.png)

---

## 🎯 Sobre o Projeto

Replicação funcional do painel administrativo do **Santander Empresas** para fins acadêmicos, construída com **Python + Django + Django Unfold + Tailwind CSS + Font Awesome**.

O objetivo é estudar:
- Autenticação em duas etapas (agência/conta → usuário/senha)
- Customização do Django Admin com o tema **Unfold**
- Layout full-width com identidade visual Santander (vermelho `#EC0000`)
- Integração com MySQL
- Templates responsivos com Tailwind
- Controle de fluxo financeiro (entradas, saídas, balanço)

---

## 🧰 Stack

| Tecnologia | Versão |
|---|---|
| Python | 3.15+ |
| Django | 6.1.2 |
| Django Unfold | 0.104+ |
| MySQL | 8.x |
| Tailwind CSS | CDN |
| Font Awesome | 6.5 |

---

## 📁 Estrutura de Pastas

```
santander/
├── manage.py
├── requirements.txt
├── .env
├── config/
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── accounts/
│   ├── models.py         # EmpresaUser (AbstractUser + CNPJ/agência/conta)
│   ├── admin.py          # Registro no Unfold
│   ├── views.py          # Login em 2 etapas + registro
│   └── urls.py
├── banking/
│   ├── models.py         # ContaEmpresarial, Movimentacao, PixChave
│   ├── admin.py          # Admin customizado com fluxo financeiro
│   ├── views.py          # Painel + dashboard_callback
│   └── urls.py
├── landing/
│   ├── views.py
│   └── urls.py
├── templates/
│   ├── base.html
│   ├── includes/
│   │   ├── header.html
│   │   └── preloader.html
│   ├── landing/index.html
│   ├── accounts/
│   │   ├── login.html
│   │   ├── login_parte_2.html
│   │   ├── register.html
│   │   ├── escolha_conta.html
│   │   └── abrir_conta_pj.html
│   ├── banking/dashboard.html
│   └── admin/
│       ├── index.html
│       └── banking/movimentacao/change_list.html
├── static/
│   ├── css/santander.css
│   ├── js/masks.js
│   └── images/
└── template.png
```

---

## 🚀 Como Executar

### 1. Clonar e entrar no diretório

```bash
cd santander
```

### 2. Criar e ativar ambiente virtual

**Windows (PowerShell):**
```powershell
python -m venv venv
venv\Scripts\activate
```

**Linux / macOS:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Instalar dependências

```bash
pip install -r requirements.txt
```

### 4. Configurar o MySQL

No **MySQL Workbench**, execute:

```sql
CREATE DATABASE santander_empresas
  CHARACTER SET utf8mb4
  COLLATE utf8mb4_unicode_ci;
```

> ⚠️ **Importante no Windows:** o MySQL não carrega as tabelas de timezone por padrão. Sem isso, o Django Admin retorna o erro `Database returned an invalid datetime value`. Baixe o pacote oficial em [dev.mysql.com/downloads/timezones.html](https://dev.mysql.com/downloads/timezones.html), importe o `.sql` **dentro do schema `mysql`** (execute `USE mysql;` antes do script).

### 5. Configurar o `.env`

```ini
SECRET_KEY=django-insecure-dev-key-change-me
DB_NAME=santander_empresas
DB_USER=root
DB_PASSWORD=sua_senha_aqui
DB_HOST=127.0.0.1
DB_PORT=3306
```

### 6. Migrar e criar superusuário

```bash
python manage.py makemigrations accounts banking
python manage.py migrate
python manage.py createsuperuser
```

### 7. Rodar

```bash
python manage.py runserver
```

---

## 🌐 URLs Principais

| URL | Descrição |
|---|---|
| `/` | Landing page institucional |
| `/accounts/register/` | Cadastro de conta PJ |
| `/accounts/abrir-conta/` | Escolha PF / PJ |
| `/accounts/abrir-conta-pj/` | Formulário CPF |
| `/accounts/login/` | Login etapa 1 (Agência + Conta) |
| `/accounts/login/usuario/` | Login etapa 2 (Usuário + Senha) |
| `/painel/` | Dashboard do cliente |
| `/admin/` | Django Admin (Unfold) |

---

## 🔐 Fluxo de Autenticação (2 etapas)

O login foi modelado como no Santander real:

1. **Etapa 1** — o cliente informa **Agência + Conta**. O sistema valida se existe um `EmpresaUser` correspondente e armazena na sessão.
2. **Etapa 2** — o cliente informa **Usuário + Senha**. O `authenticate()` do Django valida as credenciais **e** confirma que o usuário pertence à agência/conta da etapa 1.

---

## 💰 Modelos de Domínio (`banking`)

- **`ContaEmpresarial`** — vínculo `OneToOne` com o usuário, saldo e limite.
- **`Movimentacao`** — entradas e saídas com data automática.
- **`PixChave`** — chaves Pix associadas à conta.

No **Admin do Unfold**, a tela de movimentações exibe o **fluxo do mês atual** (entradas, saídas e balanço) no topo, com valores formatados em Real brasileiro.

---

## ⚙️ Configuração do Unfold

O tema do Admin é customizado em `config/settings.py` no bloco `UNFOLD`, com:
- Cores Santander (`primary.500 = 236, 0, 0` → `#EC0000`)
- Título e header "Santander Empresas"
- `DASHBOARD_CALLBACK` apontando para `banking.views.dashboard_callback`

---

## 🧪 Observações Técnicas

- **Python 3.15 exige Django 6.1+.** Versões anteriores falham na renderização do Admin por incompatibilidade com `BaseContext`.
- O **Django Unfold precisa estar atualizado** para a mesma versão do Django. Caso contrário, surgem erros como `InclusionAdminNode.__init__() missing 1 required positional argument: 'token'`.
- O **MySQL no Windows** exige importação manual das tabelas de timezone para que filtros por data no Admin funcionem.
- Formulários protegidos por `{% csrf_token %}` dentro da tag `<form>`. Em caso de erro 403 após login, recarregar a página (`Ctrl+F5`) resolve.

---

## ⚠️ Aviso Legal

Este projeto:
- **NÃO** é afiliado, patrocinado ou endossado pelo Banco Santander.
- **NÃO** deve ser usado para transações financeiras reais.
- **NÃO** armazena, coleta ou processa dados sensíveis de usuários reais.
- **NÃO** tem fins comerciais.

As marcas "Santander", "Santander Empresas" e os logotipos associados são propriedade do **Banco Santander S.A.** O uso neste repositório é restrito a **contexto educacional**, conforme o artigo 46 da Lei nº 9.610/98 (Brasil) — citação para fins de estudo.

Projeto desenvolvido como **trabalho acadêmico**, sem vínculo empregatício, comercial ou institucional com qualquer instituição financeira.