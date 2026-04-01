from gerenciamento.menu_gerenciamento import menu_gerenciamento


def main():

    while True:
        print("\n=== SISTEMA DE VOTACAO ===")
        print("1 - Gerenciamento")
        print("2 - Votacao")
        print("0 - Sair")

        op = input("Escolha: ")

        if op == "1":
            menu_gerenciamento()

        elif op == "2":
            print("\nMódulo de votação ainda não implementado.")

        elif op == "0":
            print("Saindo...")
            break

        else:
            print("Opção inválida.")


if __name__ == "__main__":
    main()