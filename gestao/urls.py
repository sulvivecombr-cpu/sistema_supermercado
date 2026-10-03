from django.urls import path
from . import views
from .views_cadastros import (
    login_view, logout_view,
    lista_produtos, produto_form, excluir_produto,
    lista_clientes, cliente_form, excluir_cliente,
    lista_funcionarios, funcionario_form, excluir_funcionario,
)
from .views_relatorios import relatorios, vendas, venda_detalhe

urlpatterns = [
    path('', views.home, name='home'),
    path('entrega/', views.registrar_entrega, name='registrar_entrega'),
    path('caixa/', views.caixa, name='caixa'),
    path('caixa/adicionar/', views.adicionar_item, name='adicionar_item'),
    path('caixa/remover/<int:index>/', views.remover_item, name='remover_item'),
    path('caixa/limpar/', views.limpar_carrinho, name='limpar_carrinho'),
    path('caixa/fechar/', views.fechar_venda, name='fechar_venda'),

    # Autenticação
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),

    # Cadastros (administrador)
    path('produtos/', lista_produtos, name='lista_produtos'),
    path('produtos/novo/', produto_form, name='novo_produto'),
    path('produtos/<int:pk>/editar/', produto_form, name='editar_produto'),
    path('produtos/<int:pk>/excluir/', excluir_produto, name='excluir_produto'),
    path('clientes/', lista_clientes, name='lista_clientes'),
    path('clientes/novo/', cliente_form, name='novo_cliente'),
    path('clientes/<int:pk>/editar/', cliente_form, name='editar_cliente'),
    path('clientes/<int:pk>/excluir/', excluir_cliente, name='excluir_cliente'),
    path('funcionarios/', lista_funcionarios, name='lista_funcionarios'),
    path('funcionarios/novo/', funcionario_form, name='novo_funcionario'),
    path('funcionarios/<int:pk>/editar/', funcionario_form, name='editar_funcionario'),
    path('funcionarios/<int:pk>/excluir/', excluir_funcionario, name='excluir_funcionario'),

    # Relatórios e histórico (administrador)
    path('relatorios/', relatorios, name='relatorios'),
    path('vendas/', vendas, name='vendas'),
    path('vendas/<int:pk>/', venda_detalhe, name='venda_detalhe'),
]
