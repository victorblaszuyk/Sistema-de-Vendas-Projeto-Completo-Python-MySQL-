import pymysql
import datetime
import sys

from dao.usuario_dao import UsuarioDAO
from dao.funcionario_dao import FuncionarioDAO
from dao.relatorio_dao import RelatorioDAO
from dao.venda_dao import VendaDAO
from dao.ferias_dao import FeriasDAO
from dao.compra_dao import CompraDAO
from dao.fornecedor_dao import FornecedorDAO
from dao.produto_dao import ProdutoDAO

from graficos import GraficosRelatorios


def conectar():
    """Conecta ao banco de dados MySQL usando pymysql."""
    try:
        conn = pymysql.connect(
            host='localhost',
            user='root',
            password='root',
            database='sistema_vendas',
            cursorclass=pymysql.cursors.DictCursor
        )
        return conn
    except pymysql.Error as e:
        print(f'Falha ao tentar estabelecer conexão com o MySQL: {e}')
        return None


def le_int(prompt: str) -> int:
    """le um inteiro com tratamento de erro."""
    try:
        return int(input(prompt))
    except ValueError:
        print("Entrada inválida. Informe um número inteiro.")
        return None


def main():
    conn = conectar()
    if conn is None:
        print("Não foi possível acessar o banco de dados. Verifique as informações de configuração.")
        sys.exit(1)

    usuarioDAO = UsuarioDAO(conn)
    funcionarioDAO = FuncionarioDAO(conn)
    relatorioDAO = RelatorioDAO(conn)
    vendaDAO = VendaDAO(conn)
    feriasDAO = FeriasDAO(conn)
    compraDAO = CompraDAO(conn)
    fornecedorDAO = FornecedorDAO(conn)
    produtoDAO = ProdutoDAO(conn)

    graficos = GraficosRelatorios(conn)

    while True:
        print("\n=== MENU PRINCIPAL ===")
        print("1. Gerenciar Usuarios")
        print("2. Gerenciar Funcionarios")
        print("3. Gerar Relatorios")
        print("4. Gerenciar Vendas")
        print("5. Gerenciar Ferias")
        print("6. Gerenciar Compras")
        print("7. Gerenciar Fornecedores")
        print("8. Gerenciar Produtos")
        print("9. Visualizar Gráficos")
        print("0. Encerrar sistema")

        opcao = le_int("Informe a opção desejada: ")
        if opcao is None:
            continue

        # 1 - USUÁRIOS
        if opcao == 1:
            print("\n=== AREA DE USUARIOS ===")
            print("1. Cadastrar novo usuario")
            print("2. Exibir lista de usuarios")
            print("3. Alterar email do usuario")
            print("4. Remover usuario")
            opcao_user = le_int("Escolha: ")
            if opcao_user is None:
                continue

            if opcao_user == 1:
                nome = input("Nome: ").strip()
                email = input("Email: ").strip()
                senha = input("Senha: ").strip()
                usuarioDAO.inserir_usuario(
                    nome, email, senha, datetime.date.today())

            elif opcao_user == 2:
                usuarios = usuarioDAO.listar_usuarios()
                for u in usuarios:
                    print(u)

            elif opcao_user == 3:
                id_user = le_int("ID do usuario: ")
                if id_user is None:
                    continue
                novo_email = input("Novo email: ").strip()
                usuarioDAO.atualizar_usuario(id_user, novo_email)

            elif opcao_user == 4:
                id_user = le_int("ID do usuario: ")
                if id_user is None:
                    continue
                usuarioDAO.deletar_usuario(id_user)

            else:
                print("Opção inválida. Tente novamente.")

        # 2 - FUNCIONÁRIOS
        elif opcao == 2:
            print("\n=== AREA DE FUNCIONARIOS ===")
            print("1. Registrar funcionario")
            print("2. Mostrar funcionarios cadastrados")
            print("3. Modificar cargo de funcionario")
            print("4. Excluir funcionario")
            opcao_func = le_int("Escolha: ")
            if opcao_func is None:
                continue

            if opcao_func == 1:
                nome = input("Nome: ").strip()
                cpf = input("CPF: ").strip()
                cargo = input("Cargo: ").strip()
                funcionarioDAO.inserir_funcionario(
                    nome, cpf, cargo, datetime.date.today(), datetime.date.today()
                )

            elif opcao_func == 2:
                funcionarios = funcionarioDAO.listar_funcionarios()
                for f in funcionarios:
                    print(f)

            elif opcao_func == 3:
                idf = le_int("ID do funcionario: ")
                if idf is None:
                    continue
                novo_cargo = input("Novo cargo: ").strip()
                funcionarioDAO.atualizar_cargo(idf, novo_cargo)

            elif opcao_func == 4:
                idf = le_int("ID do funcionario: ")
                if idf is None:
                    continue
                funcionarioDAO.deletar_funcionario(idf)

            else:
                print("Opção inválida. Tente novamente.")

        # 3 - RELATÓRIOS
        elif opcao == 3:
            print("\n=== AREA DE RELATORIOS ===")
            print("1. Vendas + Clientes + Produtos")
            print("2. Funcionarios com cargos e datas")
            print("3. Compras vinculadas ao fornecedor")
            print("4. Quantidade total vendida por produto")
            print("5. Total de vendas agrupado por cliente")
            print("6. Média de preços")
            print("7. Vendas registradas nos últimos 30 dias")
            print("8. Resumo de vendas por mês")
            print("9. Produtos adicionados recentemente")
            print("10. Clientes com mais de 5 compras")
            print("11. Produtos mais vendidos comparados com a média")
            print("12. Clientes inativos por mais de 6 meses")

            opc = le_int("Escolha a opção: ")
            if opc is None:
                continue

            try:
                match opc:
                    case 1: relatorioDAO.listar_vendas_com_cliente_e_produto()
                    case 2: relatorioDAO.listar_funcionarios_com_cargo_e_data()
                    case 3: relatorioDAO.listar_compras_com_fornecedor()
                    case 4: relatorioDAO.relatorio_group_by()
                    case 5: relatorioDAO.total_vendas_por_cliente()
                    case 6: relatorioDAO.media_preco_produto()
                    case 7: relatorioDAO.relatorio_funcoes_data()
                    case 8: relatorioDAO.relatorio_vendas_por_mes()
                    case 9: relatorioDAO.relatorio_produtos_recentes()
                    case 10: relatorioDAO.relatorio_clientes_5_compras()
                    case 11: relatorioDAO.relatorio_produtos_mais_vendidos()
                    case 12: relatorioDAO.relatorio_clientes_semcompras()
                    case _: print("Opção inexistente.")
            except AttributeError as e:
                print("Este relatório ainda não foi implementado:", e)

        # 4 - VENDAS
        elif opcao == 4:
            print("\n=== AREA DE VENDAS ===")
            print("1. Registrar venda")
            print("2. Consultar vendas")
            opc_v = le_int("Escolha: ")
            if opc_v is None:
                continue

            if opc_v == 1:
                id_usuario = le_int("ID Usuario: ")
                if id_usuario is None:
                    continue

                id_cliente = le_int("ID Cliente: ")
                if id_cliente is None:
                    continue

                try:
                    data = datetime.date.fromisoformat(
                        input("Data (AAAA-MM-DD): ").strip())
                except Exception:
                    print("Formato de data incorreto.")
                    continue

                id_produto = le_int("ID Produto: ")
                if id_produto is None:
                    continue

                qtd = le_int("Quantidade: ")
                if qtd is None:
                    continue

                try:
                    preco = float(input("Preço unitario: ").replace(",", "."))
                except ValueError:
                    print("Valor de preço inválido.")
                    continue

                vendaDAO.inserir_venda(
                    id_usuario, id_cliente, data, id_produto, qtd, preco)

            elif opc_v == 2:
                vendaDAO.listar_vendas()

        # 5 - FÉRIAS
        elif opcao == 5:
            print("\n=== AREA DE FERIAS ===")
            print("1. Registrar ferias")
            print("2. Consultar ferias")
            print("3. Alterar período de ferias")
            print("4. Remover registro de ferias")
            opc_f = le_int("Escolha: ")
            if opc_f is None:
                continue

            if opc_f == 1:
                idf = le_int("ID do funcionario: ")
                if idf is None:
                    continue

                try:
                    inicio = datetime.date.fromisoformat(
                        input("Data inicial (AAAA-MM-DD): ").strip())
                    fim = datetime.date.fromisoformat(
                        input("Data final (AAAA-MM-DD): ").strip())
                except Exception:
                    print("Formato de data inválido.")
                    continue

                feriasDAO.inserir_ferias(idf, inicio, fim)

            elif opc_f == 2:
                feriasDAO.listar_ferias()

            elif opc_f == 3:
                idfer = le_int("ID das ferias: ")
                if idfer is None:
                    continue

                try:
                    novo_i = datetime.date.fromisoformat(
                        input("Nova data inicial (AAAA-MM-DD): ").strip())
                    novo_f = datetime.date.fromisoformat(
                        input("Nova data final (AAAA-MM-DD): ").strip())
                except Exception:
                    print("Formato de data inválido.")
                    continue

                feriasDAO.atualizar_ferias(idfer, novo_i, novo_f)

            elif opc_f == 4:
                idfer = le_int("ID das ferias: ")
                if idfer is None:
                    continue
                feriasDAO.deletar_ferias(idfer)

        # 6 - COMPRAS
        elif opcao == 6:
            print("\n=== AREA DE COMPRAS ===")
            print("1. Registrar compra")
            print("2. Consultar compras")
            print("3. Modificar compra existente")
            print("4. Excluir compra")
            opc_c = le_int("Escolha: ")
            if opc_c is None:
                continue

            if opc_c == 1:
                id_for = le_int("ID do fornecedor: ")
                if id_for is None:
                    continue

                try:
                    data = datetime.date.fromisoformat(
                        input("Data (AAAA-MM-DD): ").strip())
                except Exception:
                    print("Formato de data inválido.")
                    continue

                compraDAO.inserir_compra(id_for, data)

            elif opc_c == 2:
                compraDAO.listar_compras()

            elif opc_c == 3:
                idc = le_int("ID da compra: ")
                if idc is None:
                    continue

                id_for_novo = le_int("ID do novo fornecedor: ")
                if id_for_novo is None:
                    continue

                try:
                    nova_data = datetime.date.fromisoformat(
                        input("Nova data (AAAA-MM-DD): ").strip())
                except Exception:
                    print("Formato de data inválido.")
                    continue

                compraDAO.atualizar_compra(idc, id_for_novo, nova_data)

            elif opc_c == 4:
                idc = le_int("ID da compra: ")
                if idc is None:
                    continue
                compraDAO.deletar_compra(idc)

        # 7 - FORNECEDORES
        elif opcao == 7:
            print("\n=== AREA DE FORNECEDORES ===")
            print("1. Cadastrar fornecedor")
            print("2. Consultar fornecedores")
            print("3. Modificar fornecedor")
            print("4. Excluir fornecedor")
            opc_forn = le_int("Escolha: ")
            if opc_forn is None:
                continue

            if opc_forn == 1:
                nome = input("Nome: ").strip()
                contato = input("Contato: ").strip()
                fornecedorDAO.inserir_fornecedor(nome, contato)

            elif opc_forn == 2:
                fornecedorDAO.listar_fornecedores()

            elif opc_forn == 3:
                idf = le_int("ID do fornecedor: ")
                if idf is None:
                    continue
                novo_nome = input("Novo nome: ").strip()
                fornecedorDAO.atualizar_fornecedor(idf, novo_nome)

            elif opc_forn == 4:
                idf = le_int("ID do fornecedor: ")
                if idf is None:
                    continue
                fornecedorDAO.deletar_fornecedor(idf)

        # 8 - PRODUTOS
        elif opcao == 8:
            print("\n=== AREA DE PRODUTOS ===")
            print("1. Registrar produto")
            print("2. Exibir lista de produtos")
            print("3. Alterar produto")
            print("4. Remover produto")
            opc_p = le_int("Escolha: ")
            if opc_p is None:
                continue

            if opc_p == 1:
                nome = input("Nome: ").strip()
                try:
                    preco = float(input("Preço: ").replace(",", "."))
                except ValueError:
                    print("Valor informado para o preço é inválido.")
                    continue
                produtoDAO.inserir_produto(nome, preco)

            elif opc_p == 2:
                produtoDAO.listar_produtos()

            elif opc_p == 3:
                idp = le_int("ID do produto: ")
                if idp is None:
                    continue

                novo_nome = input("Novo nome: ").strip()
                try:
                    novo_preco = float(input("Novo preço: ").replace(",", "."))
                except ValueError:
                    print("Preço informado não é válido.")
                    continue

                produtoDAO.atualizar_produto(idp, novo_nome, novo_preco)

            elif opc_p == 4:
                idp = le_int("ID do produto: ")
                if idp is None:
                    continue
                produtoDAO.deletar_produto(idp)

        # 9 - GRÁFICOS
        elif opcao == 9:
            print("\n=== AREA DE GRAFICOS ===")
            print("1. Ranking de produtos mais vendidos")
            print("2. Total de vendas por cliente")
            print("3. Resumo de faturamento mensal")

            opc_g = le_int("Escolha: ")
            if opc_g is None:
                continue

            if opc_g == 1:
                graficos.grafico_produtos_mais_vendidos()

            elif opc_g == 2:
                graficos.grafico_vendas_por_cliente()

            elif opc_g == 3:
                graficos.grafico_faturamento_mensal()

            else:
                print("Opção não reconhecida.")

        # ENCERRAR
        elif opcao == 0:
            print("Finalizando o sistema...")
            conn.close()
            break

        else:
            print("Opção inválida. Informe uma escolha válida.")


if __name__ == "__main__":
    main()
