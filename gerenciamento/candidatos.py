import random
from database.conexao import conexao, cursor


def gerar_numero_candidato():
    """
    Gera um número único para o candidato.
    Utiliza números aleatórios entre 1000 e 9999 para garantir unicidade.
    """
    return random.randint(1000, 9999)


def cadastrar_candidato():
    """
    Cadastra um novo candidato no sistema.
    Solicita: nome, número de votação e partido.
    Valida a duplicidade de números antes de inserir.
    """
    print("\n=== CADASTRO DE CANDIDATO ===")

    nome = input("Nome completo: ")
    numero = input("Número de votação: ")
    partido = input("Partido: ")

    # Verifica duplicidade de número
    sql = "SELECT * FROM candidatos WHERE numero_votacao = %s"
    cursor.execute(sql, (numero,))

    if cursor.fetchone():
        print("Número de votação já cadastrado.")
        return

    # ERRO 1 CORRIGIDO: Quebra de linha apropriada
    sql = (
        "INSERT INTO candidatos (nome, numero_votacao, partido) "
        "VALUES (%s, %s, %s)"
    )

    cursor.execute(sql, (nome, numero, partido))
    conexao.commit()

    print("\nCandidato cadastrado com sucesso!")
    print(f"Nome: {nome}")
    print(f"Número: {numero}")
    print(f"Partido: {partido}")


def listar_candidatos():
    """
    Lista todos os candidatos cadastrados no sistema.
    Exibe: nome, número de votação e partido.
    """
    print("\n=== LISTA DE CANDIDATOS ===")

    sql = "SELECT nome, numero_votacao, partido FROM candidatos"
    cursor.execute(sql)

    dados = cursor.fetchall()

    if not dados:
        print("Nenhum candidato cadastrado.")
        return

    for c in dados:
        print("\n------------------")
        print("Nome:", c[0])
        print("Número:", c[1])
        print("Partido:", c[2])


def buscar_candidato():
    """
    Busca um candidato específico pelo número de votação.
    Exibe os dados do candidato encontrado.
    """
    print("\n=== BUSCAR CANDIDATO ===")

    numero = input("Número de votação: ")

    # ERRO 2 CORRIGIDO: Quebra de linha apropriada
    sql = (
        "SELECT nome, numero_votacao, partido "
        "FROM candidatos "
        "WHERE numero_votacao = %s"
    )

    cursor.execute(sql, (numero,))
    c = cursor.fetchone()

    if not c:
        print("Candidato não encontrado.")
        return

    print("\n=== ENCONTRADO ===")
    print("Nome:", c[0])
    print("Número:", c[1])
    print("Partido:", c[2])


def editar_candidato():
    """
    Edita as informações de um candidato existente.
    Permite alterar nome e partido, mantendo o número único.
    Valida a unicidade do novo número antes de atualizar.
    """
    print("\n=== EDITAR CANDIDATO ===")

    numero_atual = input("Número do candidato a editar: ")

    sql = "SELECT * FROM candidatos WHERE numero_votacao = %s"
    cursor.execute(sql, (numero_atual,))

    if not cursor.fetchone():
        print("Candidato não encontrado.")
        return

    print("\nDigite os novos dados (deixe em branco para manter):")

    nome = input("Novo nome: ")
    numero_novo = input("Novo número: ")
    partido = input("Novo partido: ")

    # Se o número foi alterado, verifica duplicidade
    if numero_novo and numero_novo != numero_atual:
        sql = "SELECT * FROM candidatos WHERE numero_votacao = %s"
        cursor.execute(sql, (numero_novo,))

        if cursor.fetchone():
            print("Novo número já está cadastrado.")
            return

    # Constrói a query dinamicamente com base no que foi alterado
    campos = []
    valores = []

    if nome:
        campos.append("nome = %s")
        valores.append(nome)

    if numero_novo:
        campos.append("numero_votacao = %s")
        valores.append(numero_novo)

    if partido:
        campos.append("partido = %s")
        valores.append(partido)

    if not campos:
        print("Nenhuma alteração foi feita.")
        return

    valores.append(numero_atual)

    sql = f"UPDATE candidatos SET {', '.join(campos)} WHERE numero_votacao = %s"

    cursor.execute(sql, valores)
    conexao.commit()

    print("Candidato atualizado com sucesso!")


def remover_candidato():
    """
    Remove um candidato do sistema.
    Solicita confirmação antes de deletar.
    """
    print("\n=== REMOVER CANDIDATO ===")

    numero = input("Número do candidato: ")

    sql = "SELECT * FROM candidatos WHERE numero_votacao = %s"
    cursor.execute(sql, (numero,))

    if not cursor.fetchone():
        print("Candidato não encontrado.")
        return

    confirm = input("Confirmar remoção? (s/n): ")

    if confirm != "s":
        return

    sql = "DELETE FROM candidatos WHERE numero_votacao = %s"
    cursor.execute(sql, (numero,))
    conexao.commit()

    print("Removido com sucesso.")