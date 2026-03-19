from gerenciamento.menu_gerenciamento import menu_gerenciamento
from gerenciamento.eleitores import cadastrar_eleitor


def menu_principal():
    print("\n=== SISTEMA DE VOTAÇÃO ELETRÔNICA ===")
    print("1 - Gerenciamento")
    print("2 - Votação")
    print("0 - Sair")

    return input("Escolha uma opção: ")


def main():

    while True:
        opcao = menu_principal()

        if opcao == "1":

            while True:
                op = menu_gerenciamento()

                if op == "1":
                    cadastrar_eleitor()

                elif op == "2":
                    print(">> Editar Eleitor")

                elif op == "3":
                    print(">> Remover Eleitor")

                elif op == "4":
                    print(">> Buscar Eleitor")

                elif op == "5":
                    print(">> Listar Eleitores")

                elif op == "6":
                    print(">> Módulo de Candidatos")

                elif op == "0":
                    break

                else:
                    print("Opção inválida.")

        elif opcao == "2":
            print("\n>> Módulo de Votação")

        elif opcao == "0":
            print("\nSaindo do sistema...")
            break

        else:
            print("Opção inválida.")


if __name__ == "__main__":
    main()