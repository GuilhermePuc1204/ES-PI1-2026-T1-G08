from database.conexao import conexao, cursor


def numero_existe(numero):
    """
    Verifica se já existe um candidato cadastrado com o número informado.

    Consulta a tabela de candidatos buscando o número fornecido para
    impedir duplicidade no momento do cadastro.

    Args:
        numero (str): Número do candidato a ser verificado.

    Returns:
        tuple: Tupla contendo os dados do candidato encontrado, ou
        None caso o número não esteja cadastrado.
    """
    sql = "SELECT * FROM candidatos WHERE numero = %s"
    cursor.execute(sql, (numero,))
    return cursor.fetchone()


def cadastrar_candidato():
    """
    Realiza o cadastro de um novo candidato no sistema.

    Solicita nome, número e partido, valida a inexistência prévia do
    número de votação e insere o candidato na tabela do banco de dados.

    Args:
        Nenhum (a entrada é coletada via input do terminal).

    Returns:
        None: A função apenas exibe mensagens e insere o candidato no
        banco de dados.
    """
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
    """
    Lista todos os candidatos cadastrados no banco de dados.

    Consulta a tabela de candidatos e exibe nome, número e partido de
    cada um. Caso não exista nenhum candidato, informa o usuário.

    Args:
        Nenhum.

    Returns:
        None: A função apenas imprime no terminal.
    """
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
    """
    Remove um candidato cadastrado a partir do número informado.

    Solicita o número do candidato, valida sua existência no banco de
    dados, pede confirmação ao usuário e, se confirmada, executa o
    DELETE na tabela de candidatos.

    Args:
        Nenhum (a entrada é coletada via input do terminal).

    Returns:
        None: A função apenas exibe mensagens e altera o banco de dados.
    """
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


def editar_candidato():
    """
    Edita as informações de um candidato cadastrado (RF001.11).

    Localiza o candidato pelo número atual e permite alterar nome,
    número de votação e partido. O novo número é revalidado quanto à
    unicidade no banco de dados (não pode coincidir com o de outro
    candidato). Manter o valor atual é possível pressionando ENTER
    em cada campo.

    Args:
        Nenhum (a entrada é coletada via input do terminal).

    Returns:
        None: A função apenas exibe mensagens e atualiza o banco de
        dados.
    """
    print("\n=== EDITAR CANDIDATO ===")

    numero_atual = input("Digite o número do candidato a ser editado: ").strip()

    sql = "SELECT id, nome, numero, partido FROM candidatos WHERE numero = %s"
    cursor.execute(sql, (numero_atual,))
    candidato = cursor.fetchone()

    if not candidato:
        print("Candidato não encontrado.")
        return

    id_candidato, nome_atual, num_atual, partido_atual = candidato

    print(f"\nCandidato encontrado: {nome_atual} - Nº {num_atual} ({partido_atual})")
    print("(Pressione ENTER para manter o valor atual)")

    # Novo nome
    novo_nome = input(f"Nome atual ({nome_atual}). Novo nome: ").strip()
    if not novo_nome:
        novo_nome = nome_atual

    # Novo número (com revalidação de unicidade)
    novo_numero_input = input(f"Número atual ({num_atual}). Novo número: ").strip()
    if novo_numero_input:
        cursor.execute(
            "SELECT id FROM candidatos WHERE numero = %s AND id != %s",
            (novo_numero_input, id_candidato)
        )
        if cursor.fetchone():
            print("Número já cadastrado para outro candidato. Edição cancelada.")
            return
        novo_numero = novo_numero_input
    else:
        novo_numero = num_atual

    # Novo partido
    novo_partido = input(f"Partido atual ({partido_atual}). Novo partido: ").strip()
    if not novo_partido:
        novo_partido = partido_atual

    cursor.execute(
        """
        UPDATE candidatos
           SET nome = %s, numero = %s, partido = %s
         WHERE id = %s
        """,
        (novo_nome, novo_numero, novo_partido, id_candidato)
    )
    conexao.commit()

    print("\nCandidato atualizado com sucesso!")


def buscar_candidato():
    """
    Busca os dados de um candidato pelo número de votação.

    Solicita o número do candidato e exibe nome, número e partido
    correspondentes. Caso não exista, informa que o candidato não foi
    encontrado.

    Args:
        Nenhum (a entrada é coletada via input do terminal).

    Returns:
        None: A função apenas exibe os dados no terminal.
    """
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