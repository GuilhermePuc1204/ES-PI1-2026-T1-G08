def menu_principal():
    """
    Menu principal do sistema.
    """

    print("\n=== SISTEMA DE VOTAÇÃO ELETRÔNICA ===")
    print("1 - Gerenciamento")
    print("2 - Votação")
    print("0 - Sair")

    return input("Escolha uma opção: ")


def main():
    """
    Função principal do sistema.
    """

    while True:
        opcao = menu_principal()

        if opcao == "1":
            print("\n>> Módulo de Gerenciamento")
            # chamar modulo gerenciamento depois

        elif opcao == "2":
            print("\n>> Módulo de Votação")
            # chamar modulo votacao depois

        elif opcao == "0":
            print("\nSaindo do sistema...")
            break

        else:
            print("\nOpção inválida.")


if __name__ == "__main__":
    main()