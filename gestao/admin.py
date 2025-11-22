from django.contrib import admin
from .models import Cliente, Funcionario, Administrador, Produto, Estoque, Entrega, Venda, Endereco

admin.site.register(Cliente)
admin.site.register(Funcionario)
admin.site.register(Administrador)
admin.site.register(Produto)
admin.site.register(Estoque)
admin.site.register(Entrega)
admin.site.register(Venda)
admin.site.register(Endereco)