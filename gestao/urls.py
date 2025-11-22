from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('entrega/', views.registrar_entrega, name='registrar_entrega'),
    path('caixa/', views.caixa, name='caixa'),
    path('caixa/adicionar/', views.adicionar_item, name='adicionar_item'),
    path('caixa/limpar/', views.limpar_carrinho, name='limpar_carrinho'),
    path('caixa/fechar/', views.fechar_venda, name='fechar_venda'),
]