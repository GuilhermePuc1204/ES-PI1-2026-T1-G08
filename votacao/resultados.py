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
            print("\nBoletim de Urna (em desenvolvimento)")

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