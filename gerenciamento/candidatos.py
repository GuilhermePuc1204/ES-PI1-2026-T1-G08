from database.conexao import conexao, cursor


def numero_existe(numero):
    sql = "SELECT * FROM candidatos WHERE numero = %s"
    cursor.execute(sql, (numero,))
    return cursor.fetchone()


def cadastrar_candidato():

    print("\n=== CADASTRO DE CANDIDATO ===")

    nome = input("Nome: ")
    numero = input("Número: ")
    partido = input("Partido: ")

    # valida duplicidade
    if numero_existe(numero):
        print("Número já cadastrado.")
        return

    sql = "INSERT INTO candidatos (nome, numero, partido) VALUES (%s, %s, %s)"
    valores = (nome, numero, partido)

    cursor.execute(sql, valores)
    conexao.commit()

    print("Candidato cadastrado com sucesso!")


def listar_candidatos():

    print("\n=== LISTA DE CANDIDATOS ===")

    sql = "SELECT nome, numero, partido FROM candidatos"
    cursor.execute(sql)
    resultados = cursor.fetchall()

    if not resultados:
        print("Nenhum candidato cadastrado.")
        return

    for r in resultados:
        print(f"Nome: {r[0]} | Número: {r[1]} | Partido: {r[2]}")


def remover_candidato():

    print("\n=== REMOVER CANDIDATO ===")

    numero = input("Digite o número do candidato: ")

    # verifica se ja existe
    sql = "SELECT * FROM candidatos WHERE numero = %s"
    cursor.execute(sql, (numero,))
    candidato = cursor.fetchone()

    if not candidato:
        print("Candidato não encontrado.")
        return

    confirm = input("Deseja realmente remover? (s/n): ")

    if confirm.lower() == "s":
        sql = "DELETE FROM candidatos WHERE numero = %s"
        cursor.execute(sql, (numero,))
        conexao.commit()
        print("Candidato removido com sucesso!")
    else:
        print("Remoção cancelada.")


def buscar_candidato():

    print("\n=== BUSCAR CANDIDATO ===")

    numero = input("Digite o número do candidato: ")

    sql = "SELECT nome, numero, partido FROM candidatos WHERE numero = %s"
    cursor.execute(sql, (numero,))
    candidato = cursor.fetchone()

    if not candidato:
        print("Candidato não encontrado.")
        return

    print("\n=== DADOS DO CANDIDATO ===")
    print(f"Nome: {candidato[0]}")
    print(f"Número: {candidato[1]}")
    print(f"Partido: {candidato[2]}")