"""
populate_db_cruzeiro.py
Povoa o schema 'sistema_vendas' com 50 registros por tabela usando PyMySQL + Faker.
Nomes de pessoas (usuários, clientes e funcionários) são inspirados em jogadores históricos do Cruzeiro.
Também gera arquivos SQL separados 'insert_<tabela>.sql' contendo os INSERTs usados.
"""

import random
from datetime import timedelta
from faker import Faker
import pymysql
import decimal
import os

# ---------- CONFIGURAÇÃO ----------
HOST = "localhost"
USER = "root"
PASSWORD = "root"
DB = "sistema_vendas"
PORT = 3306

QTY = 50  # quantidade por tabela

fake = Faker("pt_BR")
OUT_DIR = "populatesqls"
os.makedirs(OUT_DIR, exist_ok=True)

# ---------- LISTA DE JOGADORES ----------
jogadores_cruzeiro = [
    "Matheus Pereira", "Gabigol", "Kaio Jorge", "Lucas Romero",
    "Fabrício Bruno", "Cássio", "Sinisterra", "Arroyo", "Bolasie",
    # Outros históricos
    "Alex", "Juan Pablo Sorín", "Arrascaeta", "Fábio", "Everton Ribeiro",
    "Marcelo Moreno", "Dedé", "Joãozinho", "Douglas Luiz"
]

# ---------- HELPERS ----------


def sql_value(val):
    """Retorna representação SQL segura (string com aspas ou NULL)."""
    if val is None:
        return "NULL"
    if isinstance(val, (int, float, decimal.Decimal)):
        return str(val)
    if hasattr(val, "isoformat"):
        return f"'{val.isoformat()}'"
    s = str(val).replace("'", "''")
    return f"'{s}'"


def write_sql_file(filename, lines):
    path = os.path.join(OUT_DIR, filename)
    with open(path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"[SQL] gravado: {path}")


# ---------- CONEXÃO ----------
conn = pymysql.connect(
    host=HOST, user=USER, password=PASSWORD, database=DB,
    cursorclass=pymysql.cursors.DictCursor, autocommit=True
)

# ---------- GUARDAR IDs ----------
usuarios_ids = []
clientes_ids = []
fornecedores_ids = []
produtos_ids = []
compras_ids = []
itens_compra_ids = []
funcionarios_ids = []
ferias_ids = []
vendas_ids = []
itens_venda_ids = []

sql_files = {
    "usuarios": [],
    "clientes": [],
    "fornecedores": [],
    "produtos": [],
    "compras": [],
    "itens_compra": [],
    "funcionarios": [],
    "ferias": [],
    "vendas": [],
    "itens_venda": [],
}

try:
    with conn.cursor() as cur:

        # -----------------------
        # 1) USUARIOS (50)
        # -----------------------
        print("Inserindo usuarios...")
        for _ in range(QTY):
            nome = random.choice(jogadores_cruzeiro)
            email = fake.unique.email()
            senha = fake.password(length=10)
            data_cadastro = fake.date_between(
                start_date='-2y', end_date='today')

            sql = "INSERT INTO usuarios (nome, email, senha, data_cadastro) VALUES (%s, %s, %s, %s)"
            cur.execute(sql, (nome, email, senha, data_cadastro))
            uid = cur.lastrowid
            usuarios_ids.append(uid)

            sql_files["usuarios"].append(
                f"INSERT INTO usuarios (nome, email, senha, data_cadastro) VALUES ({sql_value(nome)}, {sql_value(email)}, {sql_value(senha)}, {sql_value(data_cadastro)});"
            )

        # -----------------------
        # 2) CLIENTES (50)
        # -----------------------
        print("Inserindo clientes...")
        for _ in range(QTY):
            nome = random.choice(jogadores_cruzeiro)
            telefone = fake.phone_number()
            endereco = fake.address().replace("\n", ", ")
            data_cadastro = fake.date_between(
                start_date='-3y', end_date='today')

            sql = "INSERT INTO clientes (nome, telefone, endereco, data_cadastro) VALUES (%s, %s, %s, %s)"
            cur.execute(sql, (nome, telefone, endereco, data_cadastro))
            cid = cur.lastrowid
            clientes_ids.append(cid)

            sql_files["clientes"].append(
                f"INSERT INTO clientes (nome, telefone, endereco, data_cadastro) VALUES ({sql_value(nome)}, {sql_value(telefone)}, {sql_value(endereco)}, {sql_value(data_cadastro)});"
            )

        # -----------------------
        # 3) FORNECEDORES (50)
        # -----------------------
        print("Inserindo fornecedores...")
        for _ in range(QTY):
            nome = fake.company()
            contato = fake.phone_number()
            endereco = fake.address().replace("\n", ", ")
            data_inicio_contrato = fake.date_between(
                start_date='-5y', end_date='today')

            sql = "INSERT INTO fornecedores (nome, contato, endereco, data_inicio_contrato) VALUES (%s, %s, %s, %s)"
            cur.execute(sql, (nome, contato, endereco, data_inicio_contrato))
            fid = cur.lastrowid
            fornecedores_ids.append(fid)

            sql_files["fornecedores"].append(
                f"INSERT INTO fornecedores (nome, contato, endereco, data_inicio_contrato) VALUES ({sql_value(nome)}, {sql_value(contato)}, {sql_value(endereco)}, {sql_value(data_inicio_contrato)});"
            )

        # -----------------------
        # 4) PRODUTOS (50)
        # -----------------------
        print("Inserindo produtos...")
        categorias = ["Eletrônicos", "Alimentos", "Bebidas",
                      "Roupas", "Brinquedos", "Casa", "Beleza"]
        for _ in range(QTY):
            nome = fake.word().capitalize() + " " + fake.word().capitalize()
            categoria = random.choice(categorias)
            preco = round(random.uniform(5.0, 500.0), 2)
            quantidade_em_estoque = random.randint(10, 200)
            data_cadastro = fake.date_between(
                start_date='-2y', end_date='today')

            sql = "INSERT INTO produtos (nome, categoria, preco, quantidade_em_estoque, data_cadastro) VALUES (%s, %s, %s, %s, %s)"
            cur.execute(sql, (nome, categoria, preco,
                        quantidade_em_estoque, data_cadastro))
            pid = cur.lastrowid
            produtos_ids.append(
                {"id": pid, "preco": preco, "estoque": quantidade_em_estoque})

            sql_files["produtos"].append(
                f"INSERT INTO produtos (nome, categoria, preco, quantidade_em_estoque, data_cadastro) VALUES ({sql_value(nome)}, {sql_value(categoria)}, {sql_value(preco)}, {sql_value(quantidade_em_estoque)}, {sql_value(data_cadastro)});"
            )

        # -----------------------
        # 5) COMPRAS + ITENS_COMPRA
        # -----------------------
        print("Inserindo compras e itens_compra...")
        for _ in range(QTY):
            id_fornecedor = random.choice(fornecedores_ids)
            data_compra = fake.date_between(start_date='-2y', end_date='today')

            sql = "INSERT INTO compras (id_fornecedor, data_compra) VALUES (%s, %s)"
            cur.execute(sql, (id_fornecedor, data_compra))
            comp_id = cur.lastrowid
            compras_ids.append(comp_id)
            sql_files["compras"].append(
                f"INSERT INTO compras (id_fornecedor, data_compra) VALUES ({sql_value(id_fornecedor)}, {sql_value(data_compra)});"
            )

            itens_por_compra = random.randint(1, 3)
            for _i in range(itens_por_compra):
                prod = random.choice(produtos_ids)
                id_produto = prod["id"]
                quantidade = random.randint(1, 20)
                preco_unitario = round(
                    prod["preco"] * random.uniform(0.8, 1.2), 2)

                sql_item = "INSERT INTO itens_compra (id_compra, id_produto, quantidade, preco_unitario) VALUES (%s, %s, %s, %s)"
                cur.execute(sql_item, (comp_id, id_produto,
                            quantidade, preco_unitario))
                itens_compra_ids.append(cur.lastrowid)
                sql_files["itens_compra"].append(
                    f"INSERT INTO itens_compra (id_compra, id_produto, quantidade, preco_unitario) VALUES ({sql_value(comp_id)}, {sql_value(id_produto)}, {sql_value(quantidade)}, {sql_value(preco_unitario)});"
                )

                # atualizar estoque
                for p in produtos_ids:
                    if p["id"] == id_produto:
                        p["estoque"] += quantidade
                        break

        # -----------------------
        # 6) FUNCIONARIOS (50)
        # -----------------------
        print("Inserindo funcionarios...")
        cargos = ["Auxiliar", "Analista", "Gerente",
                  "Coordenador", "Vendedor", "Estagiário"]
        for _ in range(QTY):
            nome = random.choice(jogadores_cruzeiro)
            cpf = fake.unique.cpf()
            cargo = random.choice(cargos)
            data_admissao = fake.date_between(
                start_date='-10y', end_date='today')
            data_inicio_trabalho = data_admissao

            sql = "INSERT INTO funcionarios (nome, cpf, cargo, data_admissao, data_inicio_trabalho) VALUES (%s, %s, %s, %s, %s)"
            cur.execute(
                sql, (nome, cpf, cargo, data_admissao, data_inicio_trabalho))
            fid = cur.lastrowid
            funcionarios_ids.append(fid)
            sql_files["funcionarios"].append(
                f"INSERT INTO funcionarios (nome, cpf, cargo, data_admissao, data_inicio_trabalho) VALUES ({sql_value(nome)}, {sql_value(cpf)}, {sql_value(cargo)}, {sql_value(data_admissao)}, {sql_value(data_inicio_trabalho)});"
            )

        # -----------------------
        # 7) FERIAS (50)
        # -----------------------
        print("Inserindo ferias...")
        for _ in range(QTY):
            id_funcionario = random.choice(funcionarios_ids)
            inicio = fake.date_between(start_date='-2y', end_date='today')
            dur = random.randint(5, 30)
            fim = inicio + timedelta(days=dur-1)
            dias_ferias = dur

            sql = "INSERT INTO ferias (id_funcionario, data_inicio, data_fim, dias_ferias) VALUES (%s, %s, %s, %s)"
            cur.execute(sql, (id_funcionario, inicio, fim, dias_ferias))
            ferias_ids.append(cur.lastrowid)
            sql_files["ferias"].append(
                f"INSERT INTO ferias (id_funcionario, data_inicio, data_fim, dias_ferias) VALUES ({sql_value(id_funcionario)}, {sql_value(inicio)}, {sql_value(fim)}, {sql_value(dias_ferias)});"
            )

        # -----------------------
        # 8) VENDAS + ITENS_VENDA
        # -----------------------
        print("Inserindo vendas e itens_venda...")
        for _ in range(QTY):
            id_usuario = random.choice(usuarios_ids)
            id_cliente = random.choice(clientes_ids)
            data_venda = fake.date_between(start_date='-1y', end_date='today')

            sql = "INSERT INTO vendas (id_usuario, id_cliente, data_venda) VALUES (%s, %s, %s)"
            cur.execute(sql, (id_usuario, id_cliente, data_venda))
            venda_id = cur.lastrowid
            vendas_ids.append(venda_id)
            sql_files["vendas"].append(
                f"INSERT INTO vendas (id_usuario, id_cliente, data_venda) VALUES ({sql_value(id_usuario)}, {sql_value(id_cliente)}, {sql_value(data_venda)});"
            )

            itens_por_venda = random.randint(1, 3)
            for _i in range(itens_por_venda):
                candid = [p for p in produtos_ids if p["estoque"] > 0]
                if not candid:
                    break
                prod = random.choice(candid)
                id_produto = prod["id"]
                quantidade = random.randint(1, min(5, prod["estoque"]))
                preco_unitario = round(
                    prod["preco"] * random.uniform(0.95, 1.2), 2)

                sql_item = "INSERT INTO itens_venda (id_venda, id_produto, quantidade, preco_unitario) VALUES (%s, %s, %s, %s)"
                cur.execute(sql_item, (venda_id, id_produto,
                            quantidade, preco_unitario))
                itens_venda_ids.append(cur.lastrowid)
                sql_files["itens_venda"].append(
                    f"INSERT INTO itens_venda (id_venda, id_produto, quantidade, preco_unitario) VALUES ({sql_value(venda_id)}, {sql_value(id_produto)}, {sql_value(quantidade)}, {sql_value(preco_unitario)});"
                )

                for p in produtos_ids:
                    if p["id"] == id_produto:
                        p["estoque"] -= quantidade
                        break

    print("Povoamento concluído com sucesso!")

    # Gravar arquivos SQL
    for tabela, lines in sql_files.items():
        if lines:
            write_sql_file(f"insert_{tabela}.sql", lines)

except Exception as e:
    print("Erro durante o povoamento:", e)

finally:
    conn.close()
    print("Conexão encerrada.")
