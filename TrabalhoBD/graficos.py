import matplotlib.pyplot as plt
import os
import datetime


class GraficosRelatorios:

    def __init__(self, conn):
        self.conn = conn

        # Criar pasta automaticamente
        self.diretorio = "graficos_exportados"
        if not os.path.exists(self.diretorio):
            os.makedirs(self.diretorio)

    # ================================
    # Função auxiliar → Salvar PNG
    # ================================
    def salvar_png(self, plt, nome_base):
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        caminho = os.path.join(self.diretorio, f"{nome_base}_{timestamp}.png")
        plt.savefig(caminho, dpi=300, bbox_inches="tight")
        print(f"\n📁 Gráfico salvo em: {caminho}\n")

    # ================================
    # 1. Produtos mais vendidos (barras)
    # ================================
    def grafico_produtos_mais_vendidos(self):
        try:
            with self.conn.cursor() as cursor:
                sql = """
                SELECT p.nome, SUM(iv.quantidade) AS total_vendido
                FROM itens_venda iv
                JOIN produtos p ON iv.id_produto = p.id_produto
                GROUP BY p.id_produto, p.nome
                ORDER BY total_vendido DESC;
                """
                cursor.execute(sql)
                dados = cursor.fetchall()

            nomes = [d["nome"] for d in dados]
            totais = [d["total_vendido"] for d in dados]

            plt.figure(figsize=(12, 6))
            plt.bar(nomes, totais)
            plt.xticks(rotation=45, ha='right')
            plt.title("Produtos Mais Vendidos")
            plt.xlabel("Produto")
            plt.ylabel("Quantidade Total Vendida")
            plt.tight_layout()

            # salvar automático
            self.salvar_png(plt, "produtos_mais_vendidos")

            plt.show()

        except Exception as e:
            print("Erro ao gerar gráfico:", e)

    # =====================================
    # 2. Vendas por Cliente (barra horizontal)
    # =====================================
    def grafico_vendas_por_cliente(self):
        try:
            with self.conn.cursor() as cursor:
                sql = """
                SELECT c.nome, COUNT(v.id_venda) AS total_vendas
                FROM vendas v
                JOIN clientes c ON v.id_cliente = c.id_cliente
                GROUP BY c.id_cliente, c.nome
                ORDER BY total_vendas DESC;
                """
                cursor.execute(sql)
                dados = cursor.fetchall()

            nomes = [d["nome"] for d in dados]
            totais = [d["total_vendas"] for d in dados]

            plt.figure(figsize=(12, 6))
            plt.barh(nomes, totais)
            plt.title("Total de Vendas por Cliente")
            plt.xlabel("Quantidade de Vendas")
            plt.ylabel("Clientes")
            plt.tight_layout()

            # salvar automático
            self.salvar_png(plt, "vendas_por_cliente")

            plt.show()

        except Exception as e:
            print("Erro ao gerar gráfico:", e)

    # ================================
    # 3. Faturamento Mensal (linha)
    # ================================
    def grafico_faturamento_mensal(self):
        try:
            with self.conn.cursor() as cursor:
                sql = """
                SELECT DATE_FORMAT(v.data_venda, '%Y-%m') AS mes,
                       SUM(iv.quantidade * iv.preco_unitario) AS faturamento
                FROM vendas v
                JOIN itens_venda iv ON v.id_venda = iv.id_venda
                GROUP BY mes
                ORDER BY mes;
                """
                cursor.execute(sql)
                dados = cursor.fetchall()

            meses = [d["mes"] for d in dados]
            faturamentos = [float(d["faturamento"]) for d in dados]

            plt.figure(figsize=(12, 6))
            plt.plot(meses, faturamentos, marker='o')
            plt.title("Faturamento Mensal")
            plt.xlabel("Mês")
            plt.ylabel("Faturamento (R$)")
            plt.grid(True)
            plt.tight_layout()

            # salvar automático
            self.salvar_png(plt, "faturamento_mensal")

            plt.show()

        except Exception as e:
            print("Erro ao gerar gráfico:", e)
