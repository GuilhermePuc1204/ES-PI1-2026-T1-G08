def menu_principal():

    print("\n==============================")
    print(" SISTEMA DE VOTAÇÃO LAD.PY ")
    print("==============================")
    print("1 - Gerenciamento")
    print("2 - Votação")
    print("3 - Auditoria")
    print("0 - Sair")
    print("==============================")


def main():

    while True:
        menu_principal()

        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            print("\nAbrindo módulo de gerenciamento...")

        elif opcao == "2":
            print("\nAbrindo módulo de votação...")

        elif opcao == "3":
            print("\nAbrindo auditoria do sistema...")

        elif opcao == "0":
            print("\nEncerrando sistema...")
            break

        else:
            print("\nOpção inválida!")


if __name__ == "__main__":
    main()