from database.conexao import cursor
from utils.auditoria import registrar_evento


def boletim_urna():

    # EVENTO AUDITÁVEL: INÍCIO DA APURAÇÃO
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

    if vencedor:
        print("\n=== VENCEDOR ===")
        print(f"Nome: {vencedor[0]}")
        print(f"Número: {vencedor[1]}")
        print(f"Partido: {vencedor[2]}")
        print(f"Total: {maior} votos")

    # EVENTO AUDITÁVEL: RESULTADOS EXIBIDOS
    registrar_evento(
        "RESULTADOS_EXIBIDOS",
        "Resultados exibidos"
    )

def estatisticas_comparecimento():

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

def menu_resultados():

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
            print(estatisticas_comparecimento())

        elif op == "3":
            print("\nVotos por Partido (em desenvolvimento)")

        elif op == "4":
            print("\nValidação de Integridade (em desenvolvimento)")

        elif op == "0":
            print("Voltando...")

        else:
            print("Opção inválida.")