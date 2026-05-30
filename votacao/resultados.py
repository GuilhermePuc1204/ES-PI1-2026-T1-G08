from database.conexao import cursor
from utils.auditoria import registrar_evento


def boletim_urna():
    """
    Gera o Boletim de Urna ao final da votação.

    Consulta o total de votos recebidos por cada candidato em ordem
    alfabética, exibe a contagem de votos nulos e declara o vencedor
    da eleição informando nome, número, partido e total de votos
    obtidos. Registra evento de auditoria no início e ao final da
    apuração.

    Args:
        Nenhum.

    Returns:
        None: A função apenas imprime no terminal e registra logs.
    """
    registrar_evento(
        "APURACAO_INICIADA",
        "Apuração iniciada"
    )

    print("\n=== BOLETIM DE URNA ===")

    sql = """
    SELECT c.nome, c.numero, c.partido, COUNT(v.id) as total
    FROM candidatos c
    LEFT JOIN votos v ON c.id = v.id_candidato
    GROUP BY c.id
    ORDER BY c.nome
    """

    cursor.execute(sql)
    resultados = cursor.fetchall()

    if not resultados:
        print("Nenhum resultado encontrado.")
        return

    maior = 0
    vencedor = None

    for r in resultados:
        nome, numero, partido, total = r
        total = total if total else 0

        print(f"{nome} - {total} voto{'s' if total != 1 else ''}")

        if total > maior:
            maior = total
            vencedor = r

    cursor.execute(
        "SELECT COUNT(*) FROM votos WHERE id_candidato IS NULL"
    )
    votos_nulos = cursor.fetchone()[0]

    print(f"\nVOTOS NULOS: {votos_nulos} voto{'s' if votos_nulos != 1 else ''}")

    if vencedor:
        print("\n=== VENCEDOR ===")
        print(f"Nome: {vencedor[0]}")
        print(f"Número: {vencedor[1]}")
        print(f"Partido: {vencedor[2]}")
        print(f"Total: {maior} votos")

    registrar_evento(
        "RESULTADOS_EXIBIDOS",
        "Resultados exibidos"
    )
def estatisticas_comparecimento():
    """
    Exibe as estatísticas de comparecimento dos eleitores.

    Consulta o total de eleitores cadastrados e o total que efetivamente
    votou (status "JA_VOTOU"), calcula o número de ausentes e o
    percentual de comparecimento em relação ao total de eleitores
    aptos.

    Args:
        Nenhum.

    Returns:
        None: A função apenas imprime no terminal.
    """
    print("\n=== ESTATÍSTICAS DE COMPARECIMENTO ===")

    cursor.execute("SELECT COUNT(*) FROM eleitores")
    total_eleitores = cursor.fetchone()[0]

    cursor.execute(
        "SELECT COUNT(*) FROM eleitores WHERE status_voto = 'JA_VOTOU'"
    )

    total_votaram = cursor.fetchone()[0]

    total_ausentes = total_eleitores - total_votaram

    porcentagem = 0

    if total_eleitores > 0:
        porcentagem = (total_votaram / total_eleitores) * 100

    print(f"Total de eleitores: {total_eleitores}")
    print(f"Compareceram: {total_votaram}")
    print(f"Ausentes: {total_ausentes}")
    print(f"Percentual de comparecimento: {porcentagem:.2f}%")

def votos_por_partido():
    """
    Exibe a somatória de votos recebidos por cada partido (legenda).

    Agrupa os votos pelo partido do candidato, calcula o percentual
    sobre o total geral de votos, exibe a contagem de votos nulos e
    destaca o partido mais votado.

    Args:
        Nenhum.

    Returns:
        None: A função apenas imprime no terminal.
    """
    print("\n=== VOTOS POR PARTIDO ===")

    # Votos por partido (exclui votos nulos automaticamente)
    sql = """
    SELECT c.partido, COUNT(v.id) as total
    FROM candidatos c
    LEFT JOIN votos v ON c.id = v.id_candidato
    GROUP BY c.partido
    ORDER BY total DESC
    """

    cursor.execute(sql)
    resultados = cursor.fetchall()

    if not resultados:
        print("Nenhum resultado encontrado.")
        return

    cursor.execute("SELECT COUNT(*) FROM votos")
    total_votos = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM votos WHERE id_candidato IS NULL")
    votos_nulos = cursor.fetchone()[0]

    maior = 0
    vencedor = None

    for r in resultados:
        partido, total = r
        total = total if total else 0

        if total_votos > 0:
            percentual = (total / total_votos) * 100
            print(f"{partido}: {total} voto{'s' if total != 1 else ''} ({percentual:.1f}%)")
        else:
            print(f"{partido}: {total} voto{'s' if total != 1 else ''}")

        if total > maior:
            maior = total
            vencedor = r

    if votos_nulos > 0:
        percentual_nulo = (votos_nulos / total_votos) * 100 if total_votos > 0 else 0
        print(f"\nVOTOS NULOS: {votos_nulos} voto{'s' if votos_nulos != 1 else ''} ({percentual_nulo:.1f}%)")
    else:
        print("\nVOTOS NULOS: 0")

    if vencedor:
        print("\n=== PARTIDO MAIS VOTADO ===")
        print(f"Partido: {vencedor[0]}")
        print(f"Total: {maior} votos")


def validacao_integridade():
    """
    Emite o relatório de validação de integridade da votação.

    Compara o total de votos registrados na tabela "votos" com a
    quantidade de eleitores cujo status é "JA_VOTOU". Se os valores
    forem iguais, confirma a integridade da eleição; caso contrário,
    emite um alerta indicando a diferença encontrada.

    Args:
        Nenhum.

    Returns:
        None: A função apenas imprime o relatório no terminal.
    """
    print("\n=== VALIDAÇÃO DE INTEGRIDADE ===")

    cursor.execute("SELECT COUNT(*) FROM votos")
    total_votos = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM eleitores WHERE status_voto = 'JA_VOTOU'")
    total_votantes = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM eleitores")
    total_eleitores = cursor.fetchone()[0]

    print(f"Total de eleitores    : {total_eleitores}")
    print(f"Eleitores que votaram : {total_votantes}")
    print(f"Votos registrados     : {total_votos}")

    if total_votos == total_votantes:
        print("\nIntegridade OK: número de votos confere com eleitores que votaram.")
    else:
        diferenca = abs(total_votos - total_votantes)
        print(f"\nALERTA: inconsistência detectada! Diferença de {diferenca} registro{'s' if diferenca != 1 else ''}.")


def menu_resultados():
    """
    Exibe o menu de Resultados da Votação (RF002.03).

    Apresenta em loop as opções de Boletim de Urna, Estatísticas de
    Comparecimento, Votos por Partido e Validação de Integridade,
    direcionando para a função correspondente. Encerra ao receber "0".

    Args:
        Nenhum.

    Returns:
        None: A função não retorna valor; encerra ao sair do loop.
    """
    op = -1

    while op != "0":
        print("\n=== RESULTADOS ===")
        print("1 - Boletim de Urna")
        print("2 - Estatísticas de Comparecimento")
        print("3 - Votos por Partido")
        print("4 - Validação de Integridade")
        print("0 - Voltar")

        op = input("Escolha: ")

        if op == "1":
            boletim_urna()

        elif op == "2":
            estatisticas_comparecimento()

        elif op == "3":
            votos_por_partido()

        elif op == "4":
            validacao_integridade()

        elif op == "0":
            print("Voltando...")

        else:
            print("Opção inválida.")