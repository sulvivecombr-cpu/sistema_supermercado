from django.db import models
from django.utils import timezone

class Endereco(models.Model):
    rua = models.CharField(max_length=200)
    numero = models.IntegerField()
    bairro = models.CharField(max_length=100)
    cidade = models.CharField(max_length=100)
    cep = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.rua}, {self.numero}"

class Pessoa(models.Model):
    nome = models.CharField(max_length=200) 
    cpf = models.CharField(max_length=14, unique=True) 
    data_nasc = models.DateField() 
    sexo = models.CharField(max_length=10) 
    login = models.CharField(max_length=50, unique=True) 
    senha = models.CharField(max_length=50) 
    
    endereco = models.OneToOneField(Endereco, on_delete=models.CASCADE, null=True, blank=True) 

    class Meta:
        abstract = True

class Cliente(Pessoa):
    pontos = models.IntegerField(default=0) 
    descontos = models.IntegerField(default=0) 

    def __str__(self):
        return f"Cliente: {self.nome}"

class Funcionario(Pessoa):
    salario = models.FloatField()
    matricula = models.IntegerField(unique=True)
    carga_horaria = models.CharField(max_length=50)
    num_caixa = models.IntegerField(null=True, blank=True) 

    def __str__(self):
        return f"Func: {self.nome} (Mat: {self.matricula})"

class Administrador(Pessoa):
    salario = models.FloatField()
    matricula = models.IntegerField(unique=True)
    filial = models.CharField(max_length=100)

    def __str__(self):
        return f"Admin: {self.nome}"

class Produto(models.Model):
    cod_barras = models.IntegerField(unique=True) 
    nome_produto = models.CharField(max_length=200) 
    descricao = models.TextField() 
    preco_compra = models.FloatField() 
    preco_venda = models.FloatField() 
    tamanho = models.IntegerField(null=True, blank=True) 
    peso = models.IntegerField(null=True, blank=True) 

    def __str__(self):
        return self.nome_produto

class Estoque(models.Model):
    produto = models.OneToOneField(Produto, on_delete=models.CASCADE)
    quantidade = models.IntegerField(default=0) 
    limite_minimo = models.IntegerField(default=10)

    def __str__(self):
        return f"Estoque de {self.produto.nome_produto}: {self.quantidade}"
    
    def verificar_alarme(self):
        if self.quantidade < self.limite_minimo:
            return "ALERTA: Estoque Baixo!"
        return "Estoque OK"

class Entrega(models.Model):
    data_entrega = models.DateTimeField(default=timezone.now) 
    valor_total = models.FloatField() 
    nota_fiscal = models.CharField(max_length=100, default="000") 
    
    produtos = models.ManyToManyField(Produto, related_name='entregas')

    def __str__(self):
        return f"Entrega {self.id} - {self.data_entrega}"

class Venda(models.Model):
    funcionario = models.ForeignKey(Funcionario, on_delete=models.PROTECT) 
    cliente = models.ForeignKey(Cliente, on_delete=models.SET_NULL, null=True, blank=True) 
    data_venda = models.DateTimeField(default=timezone.now) 
    valor_total = models.FloatField(default=0.0) 
    produtos = models.ManyToManyField(Produto, through='ItemVenda') 

    def __str__(self):
        return f"Venda {self.id} por {self.funcionario.nome}"

class ItemVenda(models.Model):
    venda = models.ForeignKey(Venda, on_delete=models.CASCADE)
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE)
    quantidade = models.IntegerField(default=1)