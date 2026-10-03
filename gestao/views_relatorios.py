from django.contrib import messages
from django.db.models import Sum, F
from django.shortcuts import render, get_object_or_404
from django.utils import timezone

from .decorators import admin_required
from .models import Venda, ItemVenda, Cliente


@admin_required
def relatorios(request):
    hoje = timezone.localdate()
    inicio_mes = hoje.replace(day=1)

    vendas_hoje = Venda.objects.filter(data_venda__date=hoje)
    faturamento_hoje = vendas_hoje.aggregate(total=Sum('valor_total'))['total'] or 0

    vendas_mes = Venda.objects.filter(data_venda__gte=inicio_mes)
    faturamento_mes = vendas_mes.aggregate(total=Sum('valor_total'))['total'] or 0

    # Lucro estimado do mês: (preço vendido - preço de compra) x quantidade
    lucro_mes = (
        ItemVenda.objects
        .filter(venda__data_venda__gte=inicio_mes, preco_unitario__gt=0)
        .aggregate(
            lucro=Sum((F('preco_unitario') - F('produto__preco_compra')) * F('quantidade'))
        )['lucro']
    ) or 0

    top_produtos = (
        ItemVenda.objects
        .values('produto__nome_produto')
        .annotate(qtd_vendida=Sum('quantidade'), receita=Sum(F('preco_unitario') * F('quantidade')))
        .order_by('-qtd_vendida')[:10]
    )

    clientes_fidelidade = Cliente.objects.order_by('-pontos')

    return render(request, 'gestao/relatorios.html', {
        'hoje': hoje,
        'faturamento_hoje': faturamento_hoje,
        'vendas_hoje': vendas_hoje.count(),
        'faturamento_mes': faturamento_mes,
        'vendas_mes': vendas_mes.count(),
        'lucro_mes': lucro_mes,
        'top_produtos': top_produtos,
        'clientes_fidelidade': clientes_fidelidade,
    })


@admin_required
def vendas(request):
    data = request.GET.get('data', '')
    lista = Venda.objects.select_related('funcionario', 'cliente').order_by('-data_venda')
    if data:
        lista = lista.filter(data_venda__date=data)
    return render(request, 'gestao/vendas.html', {'vendas': lista, 'data': data})


@admin_required
def venda_detalhe(request, pk):
    venda = get_object_or_404(
        Venda.objects.select_related('funcionario', 'cliente'), pk=pk
    )
    itens = []
    for item in venda.itemvenda_set.select_related('produto').all():
        # Vendas antigas (antes do campo) usam o preço atual do produto como referência
        preco = item.preco_unitario or item.produto.preco_venda
        itens.append({'item': item, 'preco': preco, 'subtotal': preco * item.quantidade})
    return render(request, 'gestao/venda_detalhe.html', {'venda': venda, 'itens': itens})
