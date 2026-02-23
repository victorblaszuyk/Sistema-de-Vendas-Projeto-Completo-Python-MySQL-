import pymysql
from pymysql.cursors import DictCursor


class RelatorioDAO:
    def __init__(self, conn):
        self.conn = conn

    # ============================================================
    # 1 - VENDAS + CLIENTES + PRODUTOS
    # ============================================================
    def listar_vendas_com_cliente_e_produto(self):
        print("\nRelatório: Vendas com informações do Cliente e Produto (JOIN)")

        sql = """
            SELECT v.id_venda, c.nome AS cliente_nome, p.nome AS produto_nome,
                   iv.quantidade, iv.preco_unitario
            FROM vendas v
            JOIN clientes c ON v.id_cliente = c.id_cliente
            JOIN itens_venda iv ON v.id_venda = iv.id_venda
            JOIN produtos p ON iv.id_produto = p.id_produto
        """

        cursor = self.conn.cursor(DictCursor)
        cursor.execute(sql)

        for row in cursor.fetchall():
            print(
                f"Venda {row['id_venda']}: Cliente: {row['cliente_nome']}, "
                f"Produto: {row['produto_nome']}, Quantidade: {row['quantidade']}, "
                f"Preço Unitário: {row['preco_unitario']:.2f}"
            )

        cursor.close()

    # ============================================================
    # 2 - FUNCIONÁRIOS + CARGO/DATA
    # ============================================================
    def listar_funcionarios_com_cargo_e_data(self):
        print("\nRelatório: Funcionários com cargo e datas")

        sql = "SELECT nome, cargo, data_admissao, data_inicio_trabalho FROM funcionarios"

        cursor = self.conn.cursor(DictCursor)
        cursor.execute(sql)

        for row in cursor.fetchall():
            print(
                f"Nome: {row['nome']}, Cargo: {row['cargo']}, "
                f"Data Admissão: {row['data_admissao']}, "
                f"Data Início Trabalho: {row['data_inicio_trabalho']}"
            )

        cursor.close()

    # ============================================================
    # 3 - COMPRAS + FORNECEDOR
    # ============================================================
    def listar_compras_com_fornecedor(self):
        print("\nRelatório: Compras com informações do Fornecedor")

        sql = """
            SELECT c.id_compra, f.nome AS fornecedor_nome, c.data_compra
            FROM compras c
            JOIN fornecedores f ON c.id_fornecedor = f.id_fornecedor
        """

        cursor = self.conn.cursor(DictCursor)
        cursor.execute(sql)

        for row in cursor.fetchall():
            print(
                f"Compra {row['id_compra']}: Fornecedor: {row['fornecedor_nome']}"
            )
            print(f"Data Compra: {row['data_compra']}\n")

        cursor.close()

    # ============================================================
    # 4 - QUANTIDADE TOTAL DE PRODUTOS VENDIDOS (GROUP BY)
    # ============================================================
    def relatorio_group_by(self):
        print("\nRelatório: Total de produtos vendidos")

        sql = """
            SELECT p.nome AS produto, SUM(iv.quantidade) AS total_vendido
            FROM itens_venda iv
            JOIN produtos p ON iv.id_produto = p.id_produto
            GROUP BY p.id_produto
            ORDER BY total_vendido DESC
        """

        cursor = self.conn.cursor(DictCursor)
        cursor.execute(sql)

        for row in cursor.fetchall():
            print(f"{row['produto']} → {row['total_vendido']} vendidos")

        cursor.close()

    # ============================================================
    # 5 - TOTAL DE VENDAS POR CLIENTE
    # ============================================================
    def total_vendas_por_cliente(self):
        print("\nRelatório: Total de vendas por cliente")

        sql = """
            SELECT c.nome, COUNT(v.id_venda) AS total_vendas
            FROM vendas v
            JOIN clientes c ON v.id_cliente = c.id_cliente
            GROUP BY c.id_cliente
            ORDER BY total_vendas DESC
        """

        cursor = self.conn.cursor(DictCursor)
        cursor.execute(sql)

        for row in cursor.fetchall():
            print(f"{row['nome']} → {row['total_vendas']} vendas")

        cursor.close()

    # ============================================================
    # 6 - MÉDIA DE PREÇO DOS PRODUTOS
    # ============================================================
    def media_preco_produto(self):
        print("\nRelatório: Média de preço dos produtos")

        sql = """
            SELECT AVG(preco) AS media_preco
            FROM produtos
        """

        cursor = self.conn.cursor(DictCursor)
        cursor.execute(sql)

        row = cursor.fetchone()
        print(f"Média de preço: R$ {row['media_preco']:.2f}")

        cursor.close()

    # ============================================================
    # 7 - VENDAS NOS ÚLTIMOS 30 DIAS
    # ============================================================
    def relatorio_funcoes_data(self):
        print("\nRelatório: Vendas dos últimos 30 dias")

        sql = """
            SELECT COUNT(*) AS total
            FROM vendas
            WHERE data_venda >= CURDATE() - INTERVAL 30 DAY
        """

        cursor = self.conn.cursor(DictCursor)
        cursor.execute(sql)

        row = cursor.fetchone()
        print(f"Total de vendas em 30 dias: {row['total']}")

        cursor.close()

    # ============================================================
    # 8 - VENDAS POR MÊS
    # ============================================================
    def relatorio_vendas_por_mes(self):
        print("\nRelatório: Vendas por mês")

        sql = """
            SELECT DATE_FORMAT(data_venda, '%Y-%m') AS mes,
                   COUNT(*) AS total
            FROM vendas
            GROUP BY mes
            ORDER BY mes DESC
        """

        cursor = self.conn.cursor(DictCursor)
        cursor.execute(sql)

        for row in cursor.fetchall():
            print(f"{row['mes']} → {row['total']} vendas")

        cursor.close()

    # ============================================================
    # 9 - PRODUTOS CADASTRADOS RECENTEMENTE
    # ============================================================
    def relatorio_produtos_recentes(self):
        print("\nRelatório: Produtos cadastrados nos últimos 60 dias")

        sql = """
            SELECT nome, data_cadastro
            FROM produtos
            WHERE data_cadastro >= CURDATE() - INTERVAL 60 DAY
            ORDER BY data_cadastro DESC
        """

        cursor = self.conn.cursor(DictCursor)
        cursor.execute(sql)

        for row in cursor.fetchall():
            print(f"{row['nome']} → {row['data_cadastro']}")

        cursor.close()

    # ============================================================
    # 10 - CLIENTES COM +5 COMPRAS
    # ============================================================
    def relatorio_clientes_5_compras(self):
        print("\nRelatório: Clientes com mais de 5 compras")

        sql = """
            SELECT c.nome, COUNT(v.id_venda) AS total
            FROM vendas v
            JOIN clientes c ON v.id_cliente = c.id_cliente
            GROUP BY c.id_cliente
            HAVING total > 5
            ORDER BY total DESC
        """

        cursor = self.conn.cursor(DictCursor)
        cursor.execute(sql)

        for row in cursor.fetchall():
            print(f"{row['nome']} → {row['total']} compras")

        cursor.close()

    # ============================================================
    # 11 - PRODUTOS ACIMA DA MÉDIA DE PREÇO
    # ============================================================
    def relatorio_produtos_mais_vendidos(self):
        print("\nRelatório: Produtos acima da média de preço")

        sql = """
            SELECT nome, preco
            FROM produtos
            WHERE preco > (SELECT AVG(preco) FROM produtos)
            ORDER BY preco DESC
        """

        cursor = self.conn.cursor(DictCursor)
        cursor.execute(sql)

        for row in cursor.fetchall():
            print(f"{row['nome']} → R$ {row['preco']}")

        cursor.close()

    # ============================================================
    # 12 - CLIENTES SEM COMPRAS NOS ÚLTIMOS 6 MESES
    # ============================================================
    def relatorio_clientes_semcompras(self):
        print("\nRelatório: Clientes sem compras nos últimos 6 meses")

        sql = """
            SELECT c.nome
            FROM clientes c
            LEFT JOIN vendas v 
                ON c.id_cliente = v.id_cliente
                AND v.data_venda >= CURDATE() - INTERVAL 6 MONTH
            WHERE v.id_venda IS NULL
        """

        cursor = self.conn.cursor(DictCursor)
        cursor.execute(sql)

        for row in cursor.fetchall():
            print(row['nome'])

        cursor.close()
