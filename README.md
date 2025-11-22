<div align="center">

  <h1>🛒 Sistema de Gestão para Supermercado</h1>
  
  **Solução Back-end para controle de estoque, vendas e fidelidade.**

![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![Django](https://img.shields.io/badge/django-%23092E20.svg?style=for-the-badge&logo=django&logoColor=white)
![Bootstrap](https://img.shields.io/badge/bootstrap-%238511FA.svg?style=for-the-badge&logo=bootstrap&logoColor=white)
![SQLite](https://img.shields.io/badge/sqlite-%2307405e.svg?style=for-the-badge&logo=sqlite&logoColor=white)

</div>

---

## Índice

- [Sobre o Projeto](#sobre-o-projeto)
- [✨ Funcionalidades](#-funcionalidades)
- [🛠️ Tecnologias Utilizadas](#-tecnologias-utilizadas)
- [🚀 Começando](#-começando)
  - [Pré-requisitos](#pré-requisitos)
  - [Instalação](#instalação)
- [🔥 Como Usar](#-como-usar)
- [📂 Estrutura do Projeto](#-estrutura-do-projeto)
- [🤝 Como Contribuir](#-como-contribuir)
- [📄 Licença](#-licença)

---

## Sobre o Projeto

Este projeto foi desenvolvido como **Trabalho Final de Programação Back-end**. O objetivo foi criar um sistema unificado para atender as demandas dos supermercados "Primeira Luz do Dia" e "Beagás".

O sistema resolve problemas cruciais de gestão, como o controle automático de estoque via entrada de notas fiscais, alertas de estoque baixo, realização de vendas em caixa (PDV) e um sistema de fidelidade para clientes, onde compras geram pontos acumulativos. A aplicação utiliza o padrão MVT (Model-View-Template) do Django.

---

## ✨ Funcionalidades

O sistema atende aos seguintes requisitos funcionais e de negócio:

- **📦 Controle Inteligente de Estoque:**
  - Cadastro automático de novos produtos ao registrar uma entrega (se o código de barras não existir).
  - Atualização automática da quantidade em estoque.
  - **Alerta de Estoque Baixo:** O sistema avisa quando a quantidade de um produto cai abaixo do limite mínimo definido.
- **🚛 Gestão de Entregas:**
  - Registro de entradas de mercadorias com Nota Fiscal, data e valor total.
  - Cálculo automático do preço de custo e sugestão de preço de venda.
- **🛒 Frente de Caixa (PDV):**
  - Adição de itens ao carrinho de compras (sessão temporária).
  - Cálculo total da venda em tempo real.
  - Finalização de venda associando um **Funcionário** e, opcionalmente, um **Cliente**.
- **💎 Programa de Fidelidade:**
  - Clientes cadastrados acumulam pontos automaticamente.
  - Regra de negócio: Cada **R$ 10,00** em compras gera **1 ponto**.
- **👥 Gestão de Pessoas:**
  - Modelagem orientada a objetos com herança (`Pessoa` como classe abstrata).
  - Perfis distintos para **Funcionários** e **Administradores**.
  - Cadastro de **Endereço** vinculado a cada pessoa.

---

## 🛠️ Tecnologias Utilizadas

- **[Python 3.10+](https://www.python.org/)**: Linguagem base do projeto.
- **[Django 5.x](https://www.djangoproject.com/)**: Framework web de alto nível para desenvolvimento rápido e limpo.
- **[SQLite](https://www.sqlite.org/index.html)**: Banco de dados relacional (padrão do Django) para persistência dos dados.
- **[Bootstrap 5](https://getbootstrap.com/)**: Framework CSS para estilização responsiva das interfaces (templates HTML).

---

## 🚀 Começando

Siga o passo a passo abaixo para rodar a aplicação no seu ambiente local.

### Pré-requisitos

- Python instalado (versão 3.10 ou superior).
- Git instalado.

### Instalação

1.  **Clone o repositório:**

    ```bash
    git clone [https://github.com/arielm11/sistema_supermercado.git](https://github.com/arielm11/sistema_supermercado.git)
    ```

2.  **Acesse a pasta do projeto:**

    ```bash
    cd sistema_supermercado
    ```

3.  **Crie e ative um ambiente virtual (recomendado):**

    - _Windows:_
      ```bash
      python -m venv venv
      venv\Scripts\activate
      ```
    - _Linux/Mac:_
      ```bash
      python3 -m venv venv
      source venv/bin/activate
      ```

4.  **Instale as dependências:**

    ```bash
    pip install django
    ```

5.  **Execute as migrações do banco de dados:**

    ```bash
    python manage.py makemigrations
    python manage.py migrate
    ```

6.  **Crie um superusuário (para acessar o painel administrativo):**

    ```bash
    python manage.py createsuperuser
    ```

    _(Siga as instruções na tela para definir usuário, email e senha)_

7.  **Inicie o servidor de desenvolvimento:**
    ```bash
    python manage.py runserver
    ```

O sistema estará acessível em: `http://127.0.0.1:8000/`

---

## 🔥 Como Usar

1.  **Painel Administrativo:**

    - Acesse `http://127.0.0.1:8000/admin`.
    - Faça login com o superusuário criado.
    - Cadastre **Funcionários** e **Clientes** iniciais para poder operar o sistema.

2.  **Registrar Entrega (Estoque):**

    - Na página inicial, clique em **"Receber Entrega"**.
    - Insira os dados da Nota Fiscal e do produto (código de barras, preço, quantidade).
    - Se o produto não existir, preencha o nome para cadastrá-lo automaticamente.

3.  **Realizar Venda (Caixa):**

    - Na página inicial, clique em **"Caixa (Vendas)"**.
    - Insira o código de barras de um produto cadastrado e a quantidade.
    - Clique em **"+ INSERIR PRODUTO"** para adicionar ao carrinho.
    - Para fechar a conta, selecione o **Vendedor** e o **Cliente** (para pontuação) e clique em **"✅ CONCLUIR VENDA"**.

4.  **Verificar Dashboard:**
    - A página inicial (`home`) exibe alertas de estoque baixo, últimas vendas e últimas entregas realizadas.

---

## 📂 Estrutura do Projeto

A estrutura principal de diretórios é organizada da seguinte forma:

```text
sistema_supermercado/
├── db.sqlite3              # Banco de dados local
├── manage.py               # Utilitário de linha de comando do Django
├── sistema_supermercado/   # Configurações do projeto (settings, urls, wsgi)
└── gestao/                 # Aplicação principal (App)
    ├── migrations/         # Histórico de mudanças do banco de dados
    ├── templates/          # Arquivos HTML (Frontend)
    │   └── gestao/
    │       ├── caixa.html
    │       ├── entrega.html
    │       ├── home.html
    │       └── index.html
    ├── admin.py            # Registro de modelos no painel admin
    ├── apps.py             # Configuração da app
    ├── forms.py            # Formulários para entrada de dados
    ├── models.py           # Modelagem do banco de dados (Classes)
    ├── tests.py            # Testes automatizados
    ├── urls.py             # Rotas da aplicação
    └── views.py            # Lógica de controle (Controladores)
```
