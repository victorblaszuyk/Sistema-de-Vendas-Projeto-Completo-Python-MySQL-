import pymysql


class FornecedorDAO:
    def __init__(self, conn):
        self.conn = conn

    def inserir_fornecedor(self, nome, contato):
        sql = """
            INSERT INTO fornecedores (nome, contato)
            VALUES (%s, %s)
        """
        try:
            with self.conn.cursor() as cursor:
                cursor.execute(sql, (nome, contato))
            self.conn.commit()
            print("O fornecedor foi registrado com sucesso.")
        except Exception as e:
            print("Falha ao tentar registrar o fornecedor:", e)

    def listar_fornecedores(self):
        sql = "SELECT * FROM fornecedores"
        try:
            with self.conn.cursor(pymysql.cursors.DictCursor) as cursor:
                cursor.execute(sql)
                fornecedores = cursor.fetchall()

                for f in fornecedores:
                    print(
                        f"ID: {f['id_fornecedor']} | Nome: {f['nome']} | Contato: {f['contato']}"
                    )
        except Exception as e:
            print("Erro durante a tentativa de listar os fornecedores:", e)

    def atualizar_fornecedor(self, id_fornecedor, novo_nome, novo_contato):
        sql = """
            UPDATE fornecedores
            SET nome = %s, contato = %s
            WHERE id_fornecedor = %s
        """
        try:
            with self.conn.cursor() as cursor:
                cursor.execute(sql, (novo_nome, novo_contato, id_fornecedor))
            self.conn.commit()
            print("Os dados do fornecedor foram atualizados com sucesso.")
        except Exception as e:
            print("Não foi possível atualizar os dados do fornecedor:", e)

    def deletar_fornecedor(self, id_fornecedor):
        sql = "DELETE FROM fornecedores WHERE id_fornecedor = %s"
        try:
            with self.conn.cursor() as cursor:
                cursor.execute(sql, (id_fornecedor,))
            self.conn.commit()
            print("O fornecedor foi removido do sistema com êxito.")
        except Exception as e:
            print("Erro ao tentar remover o fornecedor:", e)
