import pymysql
from datetime import date


class FeriasDAO:
    def __init__(self, conn):
        self.conn = conn

    def inserir_ferias(self, id_funcionario, data_inicio, data_fim):
        # Calcula diferença em dias
        diff_dias = (data_fim - data_inicio).days + 1

        sql = """
            INSERT INTO ferias (id_funcionario, data_inicio, data_fim, dias_ferias)
            VALUES (%s, %s, %s, %s)
        """

        try:
            with self.conn.cursor() as cursor:
                cursor.execute(
                    sql, (id_funcionario, data_inicio, data_fim, diff_dias))
            self.conn.commit()
            print(
                f"As férias foram registradas com êxito. Total de dias calculados: {diff_dias}"
            )

        except Exception as e:
            print("Ocorreu um erro ao tentar registrar as férias:", e)

    def listar_ferias(self):
        sql = "SELECT * FROM ferias"

        try:
            with self.conn.cursor(pymysql.cursors.DictCursor) as cursor:
                cursor.execute(sql)
                registros = cursor.fetchall()

                for row in registros:
                    print(
                        f"ID: {row['id_ferias']} | Funcionário: {row['id_funcionario']} "
                        f"| Início: {row['data_inicio']} | Fim: {row['data_fim']} "
                        f"| Total de dias: {row['dias_ferias']}"
                    )

        except Exception as e:
            print("Não foi possível listar os registros de férias:", e)

    def atualizar_ferias(self, id_ferias, nova_data_inicio, nova_data_fim):
        sql = """
            UPDATE ferias
            SET data_inicio = %s, data_fim = %s, dias_ferias = %s
            WHERE id_ferias = %s
        """

        try:
            diff_dias = (nova_data_fim - nova_data_inicio).days + 1

            with self.conn.cursor() as cursor:
                cursor.execute(
                    sql, (nova_data_inicio, nova_data_fim, diff_dias, id_ferias))
            self.conn.commit()

            print("Os dados das férias foram atualizados com sucesso.")

        except Exception as e:
            print("Falha ao tentar atualizar os dados das férias:", e)

    def deletar_ferias(self, id_ferias):
        sql = "DELETE FROM ferias WHERE id_ferias = %s"

        try:
            with self.conn.cursor() as cursor:
                cursor.execute(sql, (id_ferias,))
            self.conn.commit()

            print("O registro de férias foi removido com sucesso.")

        except Exception as e:
            print("Não foi possível excluir o registro de férias:", e)
