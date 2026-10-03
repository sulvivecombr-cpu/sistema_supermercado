from django.contrib import messages
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.db.models import ProtectedError
from django.shortcuts import render, redirect, get_object_or_404

from .decorators import admin_required
from .forms import FormularioProduto, FormularioCliente, FormularioFuncionario
from .models import Cliente, Funcionario, Produto, Estoque


# ---------- Autenticação (apenas administrador) ----------

def login_view(request):
    if request.method == 'POST':
        usuario = authenticate(
            request,
            username=request.POST.get('username'),
            password=request.POST.get('password'),
        )
        if usuario is not None and usuario.is_staff:
            auth_login(request, usuario)
            return redirect('home')
        messages.error(request, 'Usuário ou senha inválidos.')
    return render(request, 'gestao/login.html')


def logout_view(request):
    auth_logout(request)
    messages.info(request, 'Sessão encerrada com sucesso.')
    return redirect('home')


# ---------- Produtos ----------

@admin_required
def lista_produtos(request):
    produtos = Produto.objects.select_related('estoque').order_by('nome_produto')
    busca = request.GET.get('q', '')
    if busca:
        produtos = produtos.filter(nome_produto__icontains=busca)
    return render(request, 'gestao/produtos.html', {'produtos': produtos, 'busca': busca})


@admin_required
def produto_form(request, pk=None):
    produto = get_object_or_404(Produto, pk=pk) if pk else None
    if request.method == 'POST':
        form = FormularioProduto(request.POST, instance=produto)
        if form.is_valid():
            produto = form.save()
            Estoque.objects.update_or_create(
                produto=produto,
                defaults={
                    'quantidade': form.cleaned_data['quantidade'],
                    'limite_minimo': form.cleaned_data['limite_minimo'],
                },
            )
            messages.success(request, f'Produto "{produto.nome_produto}" salvo com sucesso!')
            return redirect('lista_produtos')
    else:
        dados = {}
        if produto and hasattr(produto, 'estoque'):
            dados = {
                'quantidade': produto.estoque.quantidade,
                'limite_minimo': produto.estoque.limite_minimo,
            }
        form = FormularioProduto(instance=produto, initial=dados)
    return render(request, 'gestao/produto_form.html', {'form': form, 'produto': produto})


@admin_required
def excluir_produto(request, pk):
    produto = get_object_or_404(Produto, pk=pk)
    if produto.itemvenda_set.exists() or produto.entregas.exists():
        messages.error(
            request,
            f'"{produto.nome_produto}" possui histórico de vendas/entregas e não pode ser excluído.',
        )
    else:
        messages.success(request, f'Produto "{produto.nome_produto}" excluído.')
        produto.delete()
    return redirect('lista_produtos')


# ---------- Clientes ----------

@admin_required
def lista_clientes(request):
    clientes = Cliente.objects.order_by('nome')
    busca = request.GET.get('q', '')
    if busca:
        clientes = clientes.filter(nome__icontains=busca)
    return render(request, 'gestao/clientes.html', {'clientes': clientes, 'busca': busca})


@admin_required
def cliente_form(request, pk=None):
    cliente = get_object_or_404(Cliente, pk=pk) if pk else None
    if request.method == 'POST':
        form = FormularioCliente(request.POST, instance=cliente)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.login = obj.login or obj.cpf  # login automático: usa o CPF
            obj.save()
            messages.success(request, f'Cliente "{obj.nome}" salvo com sucesso!')
            return redirect('lista_clientes')
    else:
        form = FormularioCliente(instance=cliente)
    return render(request, 'gestao/cliente_form.html', {'form': form, 'cliente': cliente})


@admin_required
def excluir_cliente(request, pk):
    cliente = get_object_or_404(Cliente, pk=pk)
    messages.success(request, f'Cliente "{cliente.nome}" excluído.')
    cliente.delete()  # vendas antigas mantêm o registro (cliente fica nulo)
    return redirect('lista_clientes')


# ---------- Funcionários ----------

@admin_required
def lista_funcionarios(request):
    funcionarios = Funcionario.objects.order_by('nome')
    busca = request.GET.get('q', '')
    if busca:
        funcionarios = funcionarios.filter(nome__icontains=busca)
    return render(request, 'gestao/funcionarios.html', {'funcionarios': funcionarios, 'busca': busca})


@admin_required
def funcionario_form(request, pk=None):
    funcionario = get_object_or_404(Funcionario, pk=pk) if pk else None
    if request.method == 'POST':
        form = FormularioFuncionario(request.POST, instance=funcionario)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.login = obj.login or obj.cpf  # login automático: usa o CPF
            obj.save()
            messages.success(request, f'Funcionário "{obj.nome}" salvo com sucesso!')
            return redirect('lista_funcionarios')
    else:
        form = FormularioFuncionario(instance=funcionario)
    return render(request, 'gestao/funcionario_form.html', {'form': form, 'funcionario': funcionario})


@admin_required
def excluir_funcionario(request, pk):
    funcionario = get_object_or_404(Funcionario, pk=pk)
    try:
        funcionario.delete()
        messages.success(request, f'Funcionário "{funcionario.nome}" excluído.')
    except ProtectedError:
        messages.error(
            request,
            f'"{funcionario.nome}" possui vendas registradas e não pode ser excluído.',
        )
    return redirect('lista_funcionarios')
