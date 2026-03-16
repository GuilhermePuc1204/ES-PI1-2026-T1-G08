from database.conexao import conectar


def menu_principal():
    """
    Exibe o menu principal do sistema de votação no terminal.
    """

    print("\n==============================")
    print(" SISTEMA DE VOTAÇÃO LAD.PY ")
    print("==============================")
    print("1 - Gerenciamento")
    print("2 - Votação")
    print("3 - Auditoria")
    print("0 - Sair")
    print("==============================")


def main():
    """
    Função principal do sistema. Responsável por iniciar o programa,
    estabelecer conexão com o banco de dados e controlar o fluxo
    do menu principal.

    """

    # tenta conectar ao banco
    conexao = conectar()

    if conexao is None:
        print("Não foi possível conectar ao banco de dados.")
        return

    print("Conexão com o banco realizada com sucesso!")

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