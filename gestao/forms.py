from django import forms
from .models import Cliente, Funcionario

class FormularioEntrega(forms.Form):
    nota_fiscal = forms.CharField(
        label='Número da Nota Fiscal', 
        max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex: 000123'})
    )
    cod_barras = forms.IntegerField(
        label='Código de Barras',
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Escaneie ou digite'})
    )
    nome_produto = forms.CharField(
        label='Nome do Produto (Se novo)', 
        max_length=200, 
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex: Arroz 5kg'})
    )
    quantidade_chegada = forms.IntegerField(
        label='Qtd Recebida',
        widget=forms.NumberInput(attrs={'class': 'form-control'})
    )
    preco_compra = forms.FloatField(
        label='Preço de Compra (R$)',
        widget=forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'})
    )
    preco_venda = forms.FloatField(
        label='Preço de Venda (R$)', 
        required=False,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'})
    )

class FormularioItemVenda(forms.Form):
    cod_barras = forms.IntegerField(
        label='Código de Barras',
        widget=forms.NumberInput(attrs={
            'class': 'form-control form-control-lg',
            'placeholder': 'Escaneie ou digite...',
            'autofocus': 'autofocus'
        })
    )
    quantidade = forms.IntegerField(
        label='Quantidade', 
        min_value=1, 
        initial=1,
        widget=forms.NumberInput(attrs={'class': 'form-control form-control-lg'})
    )

class FormularioFecharVenda(forms.Form):
    cliente = forms.ModelChoiceField(
        queryset=Cliente.objects.all(), 
        required=False, 
        label="Cliente (Fidelidade)",
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    funcionario = forms.ModelChoiceField(
        queryset=Funcionario.objects.all(), 
        label="Funcionário Caixa",
        widget=forms.Select(attrs={'class': 'form-select'})
    )