def menu_votacao():

    op = -1

    while op != "0":
        print("\n=== VOTAÇÃO ===")
        print("1 - Abrir Sistema de Votação")
        print("2 - Auditoria da Votação")
        print("3 - Resultados da Votação")
        print("0 - Voltar")

        op = input("Escolha: ")

        if op == "1":
            print("Abrindo sistema de votação...")

        elif op == "2":
            print("Abrindo auditoria...")

        elif op == "3":
            print("Mostrando resultados...")

        elif op == "0":
            print("Voltando...")

        else:
            print("Opção inválida.")