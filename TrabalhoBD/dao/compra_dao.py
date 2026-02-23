import pymysql
from pymysql.err import MySQLError
from pymysql.cursors import DictCursor


class CompraDAO:
    def __init__(self, conn):
        self.conn = conn

    # ============================================================
    # INSERIR COMPRA
    # ============================================================
    def inserir_compra(self, id_fornecedor, data_compra):
        sql = """
            INSERT INTO compras (id_fornecedor, data_compra)
            VALUES (%s, %s)
        """
        try:
            cursor = self.conn.cursor()
            cursor.execute(sql, (id_fornecedor, data_compra))
            self.conn.commit()
            print("Compra inserida com sucesso.")
        except MySQLError as e:
            print("Erro ao inserir compra:", e)
        finally:
            cursor.close()

    # ============================================================
    # LISTAR COMPRAS + ITENS
    # ============================================================
    def listar_compras(self):
        sql = """
            SELECT 
                c.id_compra,
                c.data_compra,
                f.nome AS nome_fornecedor,

                ic.id_produto,
                p.nome AS nome_produto,
                ic.quantidade,
                ic.preco_unitario

            FROM compras c
            JOIN fornecedores f ON c.id_fornecedor = f.id_fornecedor
            JOIN itens_compra ic ON c.id_compra = ic.id_compra
            JOIN produtos p ON ic.id_produto = p.id_produto
            ORDER BY c.id_compra, ic.id_produto;
        """

        try:
            cursor = self.conn.cursor(DictCursor)
            cursor.execute(sql)

            compra_atual = None

            for row in cursor.fetchall():

                if row["id_compra"] != compra_atual:
                    compra_atual = row["id_compra"]

                    print("\n==============================")
                    print(f"Compra ID: {row['id_compra']}")
                    print(f"Data: {row['data_compra']}")
                    print(f"Fornecedor: {row['nome_fornecedor']}")
                    print("Itens:")

                print(f"  - Produto: {row['nome_produto']} (ID {row['id_produto']}), "
                      f"Qtd: {row['quantidade']}, "
                      f"Preço Unit.: R$ {row['preco_unitario']:.2f}")

        except MySQLError as e:
            print("Erro ao listar compras:", e)
        finally:
            cursor.close()

    # ============================================================
    # ATUALIZAR COMPRA
    # ============================================================
    def atualizar_compra(self, id_compra, novo_id_fornecedor, nova_data):
        sql = """
            UPDATE compras
            SET id_fornecedor = %s, data_compra = %s
            WHERE id_compra = %s
        """

        try:
            cursor = self.conn.cursor()
            cursor.execute(sql, (novo_id_fornecedor, nova_data, id_compra))
            self.conn.commit()

            if cursor.rowcount == 0:
                print("Nenhuma compra encontrada com o ID informado.")
            else:
                print("Compra atualizada com sucesso.")

        except MySQLError as e:
            print("Erro ao atualizar a compra:", e)
        finally:
            cursor.close()

    # ============================================================
    # DELETAR COMPRA
    # ============================================================
    def deletar_compra(self, id_compra):
        sql = "DELETE FROM compras WHERE id_compra = %s"

        try:
            cursor = self.conn.cursor()
            cursor.execute(sql, (id_compra,))
            self.conn.commit()

            if cursor.rowcount == 0:
                print("Nenhuma compra encontrada com o ID informado.")
            else:
                print("Compra deletada com sucesso.")

        except MySQLError as e:
            print("Erro ao deletar compra:", e)
        finally:
            cursor.close()
