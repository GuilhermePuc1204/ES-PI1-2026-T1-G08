from gerenciamento.eleitores import (
    cadastrar_eleitor,
    listar_eleitores,
    buscar_eleitor,
    remover_eleitor
)


def menu_gerenciamento():

    while True:
        print("\n=== GERENCIAMENTO ===")
        print("1 - Cadastrar eleitor")
        print("2 - Listar eleitores")
        print("3 - Buscar eleitor")
        print("4 - Remover eleitor")
        print("0 - Voltar")

        op = input("Escolha: ")

        if op == "1":
            cadastrar_eleitor()

        elif op == "2":
            listar_eleitores()

        elif op == "3":
            buscar_eleitor()

        elif op == "4":
            remover_eleitor()

        elif op == "0":
            break

        else:
            print("Opção inválida.")