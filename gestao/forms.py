from django import forms
from .models import Cliente, Funcionario, Produto

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
    pontos_resgatar = forms.IntegerField(
        label='Resgatar Pontos (R$ 1,00 por ponto)',
        required=False,
        min_value=0,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Opcional — mínimo 10 pontos'
        })
    )

class FormularioProduto(forms.ModelForm):
    quantidade = forms.IntegerField(
        label='Quantidade em Estoque', initial=0,
        widget=forms.NumberInput(attrs={'class': 'form-control'})
    )
    limite_minimo = forms.IntegerField(
        label='Limite Mínimo (Alerta de Estoque)', initial=10,
        widget=forms.NumberInput(attrs={'class': 'form-control'})
    )

    class Meta:
        model = Produto
        fields = ['cod_barras', 'nome_produto', 'descricao', 'preco_compra', 'preco_venda']
        widgets = {
            'cod_barras': forms.NumberInput(attrs={'class': 'form-control'}),
            'nome_produto': forms.TextInput(attrs={'class': 'form-control'}),
            'descricao': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
            'preco_compra': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'preco_venda': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
        }

class FormularioCliente(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = ['nome', 'cpf', 'data_nasc', 'sexo']
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control'}),
            'cpf': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex: 123.456.789-00'}),
            'data_nasc': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'sexo': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex: Masculino / Feminino'}),
        }

class FormularioFuncionario(forms.ModelForm):
    class Meta:
        model = Funcionario
        fields = ['nome', 'cpf', 'data_nasc', 'sexo', 'salario', 'matricula', 'carga_horaria', 'num_caixa']
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control'}),
            'cpf': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex: 123.456.789-00'}),
            'data_nasc': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'sexo': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex: Masculino / Feminino'}),
            'salario': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'matricula': forms.NumberInput(attrs={'class': 'form-control'}),
            'carga_horaria': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex: 44h semanais'}),
            'num_caixa': forms.NumberInput(attrs={'class': 'form-control'}),
        }
