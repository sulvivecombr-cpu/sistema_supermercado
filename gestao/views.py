from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import FormularioEntrega, FormularioItemVenda, FormularioFecharVenda
from .models import Produto, Estoque, Entrega, Venda, ItemVenda, Cliente, Funcionario
from django.utils import timezone
from django.db.models import F

def home(request):
    estoque_baixo = Estoque.objects.filter(quantidade__lt=F('limite_minimo'))

    ultimas_vendas = Venda.objects.order_by('-data_venda')[:5]

    ultimas_entregas = Entrega.objects.order_by('-data_entrega')[:5]

    return render(request, 'gestao/home.html', {
        'estoque_baixo': estoque_baixo,
        'ultimas_vendas': ultimas_vendas,
        'ultimas_entregas': ultimas_entregas
    })

def registrar_entrega(request):
    if request.method == 'POST':
        form = FormularioEntrega(request.POST)
        if form.is_valid():
            dados = form.cleaned_data
            
            cod = dados['cod_barras']
            qtd = dados['quantidade_chegada']
            
            produto_obj = None
            
            try:
                produto_obj = Produto.objects.get(cod_barras=cod)
            except Produto.DoesNotExist:
                if not dados['nome_produto']:
                    messages.error(request, "Produto novo! É preciso preencher o Nome.")
                    return render(request, 'gestao/entrega.html', {'form': form})
                
                produto_obj = Produto.objects.create(
                    cod_barras=cod,
                    nome_produto=dados['nome_produto'],
                    preco_compra=dados['preco_compra'],
                    preco_venda=dados['preco_venda'] if dados['preco_venda'] else 0,
                    descricao="Cadastrado via entrega", 
                    tamanho=0, peso=0 
                )
                Estoque.objects.create(produto=produto_obj, quantidade=0)
            
            estoque_obj = Estoque.objects.get(produto=produto_obj)
            estoque_obj.quantidade += qtd
            estoque_obj.save()
            
            
            nova_entrega = Entrega.objects.create(
                valor_total=dados['preco_compra'] * qtd,
                nota_fiscal=dados['nota_fiscal'],
                data_entrega=timezone.now()
            )
            nova_entrega.produtos.add(produto_obj)
            
            messages.success(request, f"Entrega processada! Estoque de {produto_obj.nome_produto} agora é {estoque_obj.quantidade}.")
            return redirect('registrar_entrega')
            
    else:
        form = FormularioEntrega()

    return render(request, 'gestao/entrega.html', {'form': form})

def caixa(request):
    if 'carrinho' not in request.session:
        request.session['carrinho'] = []
    
    carrinho = request.session['carrinho']
    valor_total_carrinho = sum(item['total'] for item in carrinho)
    
    form_item = FormularioItemVenda()
    form_fechar = FormularioFecharVenda()
    
    return render(request, 'gestao/caixa.html', {
        'carrinho': carrinho,
        'valor_total': valor_total_carrinho,
        'form_item': form_item,
        'form_fechar': form_fechar
    })

def adicionar_item(request):
    if request.method == 'POST':
        form = FormularioItemVenda(request.POST)
        if form.is_valid():
            cod = form.cleaned_data['cod_barras']
            qtd = form.cleaned_data['quantidade']
            
            try:
                produto = Produto.objects.get(cod_barras=cod)
                estoque = Estoque.objects.get(produto=produto)
                
                if estoque.quantidade >= qtd:
                    item = {
                        'cod_barras': produto.cod_barras,
                        'nome': produto.nome_produto,
                        'preco_unitario': produto.preco_venda,
                        'quantidade': qtd,
                        'total': produto.preco_venda * qtd
                    }
                    carrinho = request.session.get('carrinho', [])
                    carrinho.append(item)
                    request.session['carrinho'] = carrinho
                else:
                    messages.error(request, f"Estoque insuficiente! Restam apenas {estoque.quantidade}.")
                    
            except Produto.DoesNotExist:
                messages.error(request, "Produto não encontrado.")
                
    return redirect('caixa')

def limpar_carrinho(request):
    if 'carrinho' in request.session:
        del request.session['carrinho']
    return redirect('caixa')

def fechar_venda(request):
    if request.method == 'POST':
        form = FormularioFecharVenda(request.POST)
        carrinho = request.session.get('carrinho', [])
        
        if not carrinho:
            messages.error(request, "O carrinho está vazio.")
            return redirect('caixa')

        if form.is_valid():
            cliente = form.cleaned_data['cliente']
            funcionario = form.cleaned_data['funcionario']
            valor_total = sum(item['total'] for item in carrinho)
            
            nova_venda = Venda.objects.create(
                funcionario=funcionario,
                cliente=cliente,
                valor_total=valor_total,
                data_venda=timezone.now()
            )
            
            for item in carrinho:
                produto = Produto.objects.get(cod_barras=item['cod_barras'])
                
                ItemVenda.objects.create(
                    venda=nova_venda,
                    produto=produto,
                    quantidade=item['quantidade']
                )
                
                estoque = Estoque.objects.get(produto=produto)
                estoque.quantidade -= item['quantidade']
                estoque.save()
                
                aviso = estoque.verificar_alarme()
                if "ALERTA" in aviso:
                    messages.warning(request, f"Atenção: {produto.nome_produto} ficou com estoque baixo!")

            if cliente:
                pontos_ganhos = int(valor_total // 10)
                cliente.pontos += pontos_ganhos
                cliente.save()
                messages.success(request, f"Venda realizada! Cliente {cliente.nome} ganhou {pontos_ganhos} pontos.")
            else:
                messages.success(request, "Venda realizada com sucesso!")
            
            del request.session['carrinho']
            
    return redirect('caixa')