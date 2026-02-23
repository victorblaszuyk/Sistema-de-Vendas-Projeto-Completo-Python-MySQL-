import pymysql
from datetime import date


class UsuarioDAO:
    def __init__(self, conn):
        self.conn = conn

    # CREATE
    def inserir_usuario(self, nome, email, senha, data_cadastro):
        sql = """
            INSERT INTO usuarios (nome, email, senha, data_cadastro)
            VALUES (%s, %s, %s, %s)
        """

        try:
            with self.conn.cursor() as cursor:
                cursor.execute(sql, (nome, email, senha, data_cadastro))
            self.conn.commit()
            print("O usuário foi cadastrado com sucesso.")
        except Exception as e:
            print("Ocorreu um erro ao tentar cadastrar o usuário:", e)

    # READ
    def listar_usuarios(self):
        sql = "SELECT * FROM usuarios"
        usuarios = []

        try:
            with self.conn.cursor(pymysql.cursors.DictCursor) as cursor:
                cursor.execute(sql)
                for row in cursor.fetchall():
                    usuarios.append(
                        f"ID: {row['id_usuario']}, "
                        f"Nome: {row['nome']}, "
                        f"Email: {row['email']}, "
                        f"Data de Cadastro: {row['data_cadastro']}"
                    )
        except Exception as e:
            print("Não foi possível listar os usuários:", e)

        return usuarios

    # UPDATE
    def atualizar_usuario(self, id_usuario, novo_email):
        sql = """
            UPDATE usuarios
            SET email = %s
            WHERE id_usuario = %s
        """

        try:
            with self.conn.cursor() as cursor:
                cursor.execute(sql, (novo_email, id_usuario))
            self.conn.commit()
            print("Os dados do usuário foram atualizados com êxito.")
        except Exception as e:
            print("Falha ao tentar atualizar os dados do usuário:", e)

    # DELETE
    def deletar_usuario(self, id_usuario):
        sql = "DELETE FROM usuarios WHERE id_usuario = %s"

        try:
            with self.conn.cursor() as cursor:
                cursor.execute(sql, (id_usuario,))
            self.conn.commit()
            print("O usuário foi removido do sistema.")
        except Exception as e:
            print("Erro ao tentar remover o usuário:", e)
