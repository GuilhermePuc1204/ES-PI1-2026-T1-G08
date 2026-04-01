import random
from database.conexao import conexao, cursor


def gerar_chave(nome):
    """
    Gera chave de acesso:
    2 letras do primeiro nome + 1 do segundo + 4 números
    """

    partes = nome.upper().split()

    if len(partes) < 2:
        return None

    chave = (
        partes[0][:2] +
        partes[1][0] +
        str(random.randint(1000, 9999))
    )

    return chave


def cadastrar_eleitor():
    """
    Cadastra um novo eleitor no banco de dados
    """

    print("\n=== CADASTRO DE ELEITOR ===")

    nome = input("Nome completo: ")
    cpf = input("CPF: ")
    titulo = input("Título de eleitor: ")
    mesario = input("É mesário? (s/n): ").lower() == "s"

    # verifica duplicidade
    sql = "SELECT * FROM eleitores WHERE cpf = %s OR titulo_eleitor = %s"
    cursor.execute(sql, (cpf, titulo))

    if cursor.fetchone():
        print("CPF ou título já cadastrado.")
        return

    # gera chave
    chave = gerar_chave(nome)

    if not chave:
        print("Erro ao gerar chave. Nome inválido.")
        return

    # insert no banco
    sql = """
    INSERT INTO eleitores (nome, cpf, titulo_eleitor, mesario, chave_acesso)
    VALUES (%s, %s, %s, %s, %s)
    """

    cursor.execute(sql, (nome, cpf, titulo, mesario, chave))
    conexao.commit()

    print("\nEleitor cadastrado com sucesso!")
    print("Chave de acesso:", chave)


def listar_eleitores():
    """
    Lista todos os eleitores cadastrados
    """

    print("\n=== LISTA DE ELEITORES ===")

    sql = "SELECT nome, cpf, titulo_eleitor, mesario, status_voto FROM eleitores"
    cursor.execute(sql)

    resultados = cursor.fetchall()

    if not resultados:
        print("Nenhum eleitor cadastrado.")
        return

    for e in resultados:
        print("------------------------")
        print("Nome:", e[0])
        print("CPF:", e[1])
        print("Título:", e[2])
        print("Mesário:", "Sim" if e[3] else "Não")
        print("Status:", e[4])


def menu_gerenciamento():
    """
    Menu do módulo de gerenciamento
    """

    while True:
        print("\n=== GERENCIAMENTO ===")
        print("1 - Cadastrar eleitor")
        print("2 - Listar eleitores")
        print("0 - Voltar")

        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            cadastrar_eleitor()

        elif opcao == "2":
            listar_eleitores()

        elif opcao == "0":
            break

        else:
            print("Opção inválida.")