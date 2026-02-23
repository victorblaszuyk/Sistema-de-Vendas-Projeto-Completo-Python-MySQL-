# Sistema de Vendas — Projeto Completo (Python + MySQL)

Este projeto implementa um Sistema de Vendas completo, utilizando Python, MySQL, DAO Pattern e geração automática de gráficos PNG.
Inclui também scripts SQL, popular automático do banco de dados e toda a estrutura organizada em módulos.

---------------------//---------------------

Estrutura do Projeto:

TrabalhoBD
│
├── __pycache__/
│
├── dao/
│   ├── compra_dao.py
│   ├── ferias_dao.py
│   ├── fornecedor_dao.py
│   ├── funcionario_dao.py
│   ├── produto_dao.py
│   ├── relatorio_dao.py
│   ├── usuario_dao.py
│   ├── venda_dao.py
│
├── graficos_exportados/
│
├── populatesqls/
│   ├── insert_clientes.sql
│   ├── insert_compras.sql
│   ├── insert_ferias.sql
│   ├── insert_fornecedores.sql
│   ├── insert_funcionarios.sql
│   ├── insert_itens_compra.sql
│   ├── insert_itens_venda.sql
│   ├── insert_produtos.sql
│   ├── insert_usuarios.sql
│   ├── insert_vendas.sql
│
├── Tabelas/
│   ├── sistema_vendas_clientes.sql
│   ├── sistema_vendas_compras.sql
│   ├── sistema_vendas_ferias.sql
│   ├── sistema_vendas_fornecedores.sql
│   ├── sistema_vendas_funcionarios.sql
│   ├── sistema_vendas_itens_compra.sql
│   ├── sistema_vendas_itens_venda.sql
│   ├── sistema_vendas_produtos.sql
│   ├── sistema_vendas_usuarios.sql
│   ├── sistema_vendas_vendas.sql
│
├── graficos.py
├── main.py
├── popular_bd.py

---------------------//---------------------

Instalação das Dependências

Execute no terminal:

pip install pymysql faker matplotlib

---------------------//---------------------

Script de Criação do Banco de Dados (MySQL):

Copie todo o conteudo presente no arquivo Script Criar Bando de Dados.txt, dentro da pasta do projeto, cole no Workbench e execute.

---------------------//---------------------

Populando o Banco de Dados Automaticamente

O arquivo:

popular_bd.py, gera automaticamente 50 registros em cada tabela, usando Faker, e também gera os arquivos SQL dentro de /populatesqls/, execute-o.

---------------------//---------------------

Executando o Sistema Principal:

main.py, a conexão com o banco de dados está nesse arquivo, antes de executa-lo é necessário edita-lo em algum leitor de codigo para fazer a conexão funcionar.
Logo no início você vai se deparar com a conexão (é a primeira função), você deve editar e ficar algo parecido com isso:

import pymysql

def conectar():
    return pymysql.connect(
        host="localhost",
        user="root",
        password="SUA_SENHA_AQUI",
        database="sistema_vendas",
        cursorclass=pymysql.cursors.DictCursor
    )


---------------------//---------------------

Padrão DAO

O sistema utiliza os DAOs para:
-cadastrar produtos
-registrar vendas
-cadastrar funcionários
-gerar relatórios
-exibir gráficos

Todos os módulos do banco de dados seguem o padrão DAO:
dao/
│ compra_dao.py
│ ferias_dao.py
│ fornecedor_dao.py
│ funcionario_dao.py
│ produto_dao.py
│ relatorio_dao.py
│ usuario_dao.py
│ venda_dao.py

Cada DAO contém:
-conexão com MySQL
-métodos CRUD específicos para cada tabela
-consultas personalizadas
-suporte para relatórios
