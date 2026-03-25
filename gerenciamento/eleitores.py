import random
from database.conexao import conectar


def gerar_chave(nome):
    """
    Gera chave de acesso dessa forma:
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


def cpf_existe(cpf, cursor):
    sql = "SELECT * FROM eleitores WHERE cpf = %s"
    cursor.execute(sql, (cpf,))
    return cursor.fetchone() is not None


def titulo_existe(titulo, cursor):
    sql = "SELECT * FROM eleitores WHERE titulo_eleitor = %s"
    cursor.execute(sql, (titulo,))
    return cursor.fetchone() is not None


def cadastrar_eleitor():

    print("\n=== CADASTRO DE ELEITOR ===")

    nome = input("Nome completo: ")
    cpf = input("CPF: ")
    titulo = input("Título de eleitor: ")
    mesario = input("É mesário? (s/n): ").lower() == "s"

    con = conectar()

    if con is None:
        print("Erro na conexão com o banco.")
        return

    cursor = con.cursor()

    # duplicidade
    if cpf_existe(cpf, cursor):
        print("CPF já cadastrado.")
        con.close()
        return

    if titulo_existe(titulo, cursor):
        print("Título já cadastrado.")
        con.close()
        return

    # gerar chave
    chave = gerar_chave(nome)

    if not chave:
        print("Erro ao gerar chave. Nome inválido.")
        con.close()
        return

    # inserir no banco
    sql = """
    INSERT INTO eleitores (nome, cpf, titulo_eleitor, mesario, chave_acesso)
    VALUES (%s, %s, %s, %s, %s)
    """

    cursor.execute(sql, (nome, cpf, titulo, mesario, chave))

    con.commit()
    con.close()

    print("\nEleitor cadastrado com sucesso!")
    print("Chave de acesso:", chave)