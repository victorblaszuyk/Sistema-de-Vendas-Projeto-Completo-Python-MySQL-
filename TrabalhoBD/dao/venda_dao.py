import pymysql


class VendaDAO:
    def __init__(self, conn):
        self.conn = conn

    # ==============================
    # INSERIR VENDA COMPLETA
    # ==============================
    def inserir_venda(self, id_usuario, id_cliente, data_venda,
                      id_produto, quantidade, preco_unitario):

        try:
            # Controle manual de transação
            self.conn.autocommit(False)

            with self.conn.cursor() as cursor:

                # 1. Inserir venda
                sql_venda = """
                    INSERT INTO vendas (id_usuario, id_cliente, data_venda)
                    VALUES (%s, %s, %s)
                """
                cursor.execute(sql_venda, (id_usuario, id_cliente, data_venda))

                id_venda = cursor.lastrowid
                if not id_venda:
                    print("Falha ao gerar o ID da venda.")
                    self.conn.rollback()
                    self.conn.autocommit(True)
                    return False

                # 2. Inserir item
                sql_item = """
                    INSERT INTO itens_venda (id_venda, id_produto, quantidade, preco_unitario)
                    VALUES (%s, %s, %s, %s)
                """
                cursor.execute(sql_item, (id_venda, id_produto,
                               quantidade, preco_unitario))

                # 3. Atualizar estoque
                sql_estoque = """
                    UPDATE produtos 
                    SET quantidade_em_estoque = quantidade_em_estoque - %s
                    WHERE id_produto = %s AND quantidade_em_estoque >= %s
                """

                cursor.execute(
                    sql_estoque, (quantidade, id_produto, quantidade))

                if cursor.rowcount == 0:
                    print(
                        f"Estoque insuficiente para o produto de ID {id_produto}.")
                    self.conn.rollback()
                    self.conn.autocommit(True)
                    return False

            # Se chegou até aqui → sucesso
            self.conn.commit()
            self.conn.autocommit(True)
            print("A venda foi registrada com êxito.")
            return True

        except Exception as e:
            print("Ocorreu um erro ao registrar a venda:", e)
            self.conn.rollback()
            self.conn.autocommit(True)
            return False

    # ==============================
    # LISTAR VENDAS COMPLETAS
    # ==============================
    def listar_vendas(self):
        sql = """
            SELECT v.id_venda, v.data_venda,
                   u.nome AS nome_usuario,
                   c.nome AS nome_cliente,
                   iv.id_produto,
                   p.nome AS nome_produto,
                   iv.quantidade,
                   iv.preco_unitario
            FROM vendas v
            JOIN usuarios u ON v.id_usuario = u.id_usuario
            JOIN clientes c ON v.id_cliente = c.id_cliente
            JOIN itens_venda iv ON v.id_venda = iv.id_venda
            JOIN produtos p ON iv.id_produto = p.id_produto
            ORDER BY v.id_venda
        """

        try:
            with self.conn.cursor(pymysql.cursors.DictCursor) as cursor:
                cursor.execute(sql)
                resultado = cursor.fetchall()

                if not resultado:
                    print("Nenhum registro de venda foi encontrado.")
                    return

                venda_atual = -1

                for row in resultado:
                    if row["id_venda"] != venda_atual:
                        venda_atual = row["id_venda"]
                        print("\n==============================")
                        print(f"Venda ID: {row['id_venda']}")
                        print(f"Data da Venda: {row['data_venda']}")
                        print(f"Responsável: {row['nome_usuario']}")
                        print(f"Cliente: {row['nome_cliente']}")
                        print("Itens da Venda:")

                    print(
                        f"   Produto: {row['nome_produto']} (ID {row['id_produto']}) | "
                        f"Quantidade: {row['quantidade']} | "
                        f"Valor Unitário: R$ {row['preco_unitario']:.2f}"
                    )

        except Exception as e:
            print("Não foi possível listar as vendas:", e)
