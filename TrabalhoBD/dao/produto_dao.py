import pymysql


class ProdutoDAO:
    def __init__(self, conn):
        self.conn = conn

    # CREATE
    def inserir_produto(self, nome, preco):
        sql = "INSERT INTO produtos (nome, preco) VALUES (%s, %s)"
        try:
            with self.conn.cursor() as cursor:
                cursor.execute(sql, (nome, preco))
            self.conn.commit()
            print("O produto foi cadastrado com sucesso.")
        except Exception as e:
            print("Falha ao tentar cadastrar o produto:", e)

    # READ
    def listar_produtos(self):
        sql = "SELECT * FROM produtos"
        try:
            with self.conn.cursor(pymysql.cursors.DictCursor) as cursor:
                cursor.execute(sql)
                produtos = cursor.fetchall()

                for p in produtos:
                    print(
                        f"ID: {p['id_produto']} | Nome: {p['nome']} | Preço: {p['preco']:.2f} | "
                        f"Estoque: {p['quantidade_em_estoque']}"
                    )
        except Exception as e:
            print("Erro ao tentar listar os produtos:", e)

    # UPDATE
    def atualizar_produto(self, id_produto, novo_nome, novo_preco):
        sql = "UPDATE produtos SET nome = %s, preco = %s WHERE id_produto = %s"
        try:
            with self.conn.cursor() as cursor:
                cursor.execute(sql, (novo_nome, novo_preco, id_produto))
            self.conn.commit()
            print("Os dados do produto foram atualizados corretamente.")
        except Exception as e:
            print("Não foi possível atualizar os dados do produto:", e)

    # DELETE
    def deletar_produto(self, id_produto):
        sql = "DELETE FROM produtos WHERE id_produto = %s"
        try:
            with self.conn.cursor() as cursor:
                cursor.execute(sql, (id_produto,))
            self.conn.commit()
            print("O produto foi removido do sistema.")
        except Exception as e:
            print("Erro ao tentar remover o produto:", e)
