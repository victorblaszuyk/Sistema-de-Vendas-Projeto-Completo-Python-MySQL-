import pymysql


class FuncionarioDAO:
    def __init__(self, conn):
        self.conn = conn

    # CREATE
    def inserir_funcionario(self, nome, cpf, cargo, data_admissao, data_inicio_trabalho):
        sql = """
            INSERT INTO funcionarios 
            (nome, cpf, cargo, data_admissao, data_inicio_trabalho)
            VALUES (%s, %s, %s, %s, %s)
        """

        try:
            with self.conn.cursor() as cursor:
                cursor.execute(
                    sql, (nome, cpf, cargo, data_admissao, data_inicio_trabalho))
            self.conn.commit()
            print("O funcionário foi registrado com sucesso.")
        except Exception as e:
            print("Ocorreu um erro ao tentar registrar o funcionário:", e)

    # READ
    def listar_funcionarios(self):
        sql = "SELECT * FROM funcionarios"
        funcionarios = []

        try:
            with self.conn.cursor(pymysql.cursors.DictCursor) as cursor:
                cursor.execute(sql)
                for row in cursor.fetchall():
                    funcionarios.append(
                        f"ID: {row['id_funcionario']}, "
                        f"Nome: {row['nome']}, "
                        f"CPF: {row['cpf']}, "
                        f"Cargo: {row['cargo']}, "
                        f"Data de Admissão: {row['data_admissao']}, "
                        f"Início do Trabalho: {row['data_inicio_trabalho']}"
                    )
        except Exception as e:
            print("Falha ao tentar listar os funcionários:", e)

        return funcionarios

    # UPDATE
    def atualizar_cargo(self, id_funcionario, novo_cargo):
        sql = "UPDATE funcionarios SET cargo = %s WHERE id_funcionario = %s"

        try:
            with self.conn.cursor() as cursor:
                cursor.execute(sql, (novo_cargo, id_funcionario))
            self.conn.commit()
            print("O cargo do funcionário foi atualizado com êxito.")
        except Exception as e:
            print("Não foi possível atualizar o cargo do funcionário:", e)

    # DELETE
    def deletar_funcionario(self, id_funcionario):
        sql = "DELETE FROM funcionarios WHERE id_funcionario = %s"

        try:
            with self.conn.cursor() as cursor:
                cursor.execute(sql, (id_funcionario,))
            self.conn.commit()
            print("O registro do funcionário foi removido com sucesso.")
        except Exception as e:
            print("Erro ao tentar excluir o funcionário:", e)
