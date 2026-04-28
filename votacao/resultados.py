from database.conexao import cursor

def boletim_urna():

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

    maior = 0
    vencedor = None

    for r in resultados:
        nome, numero, partido, total = r
        total = total if total else 0

        print(f"{nome} - {total} votos")

        if total > maior:
            maior = total
            vencedor = r

    if vencedor:
        print("\n=== VENCEDOR ===")
        print(f"Nome: {vencedor[0]}")
        print(f"Número: {vencedor[1]}")
        print(f"Partido: {vencedor[2]}")
        print(f"Total: {maior} votos")


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
            print("\nEstatísticas de Comparecimento (em desenvolvimento)")

        elif op == "3":
            print("\nVotos por Partido (em desenvolvimento)")

        elif op == "4":
            print("\nValidação de Integridade (em desenvolvimento)")

        elif op == "0":
            print("Voltando...")

        else:
            print("Opção inválida.")