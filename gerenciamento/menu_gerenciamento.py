from gerenciamento.candidatos import (cadastrar_candidato, listar_candidatos, remover_candidato)
from gerenciamento.eleitores import (
    cadastrar_eleitor,
    listar_eleitores,
    buscar_eleitor,
    remover_eleitor
)

def menu_gerenciamento():

    op = -1  # inicializa a variável

    while op != "0":
        print("\n=== GERENCIAMENTO ===")
        print("1 - Cadastrar eleitor")
        print("2 - Listar eleitores")
        print("3 - Buscar eleitor")
        print("4 - Remover eleitor")
        print("5 - Cadastrar candidato")
        print("6 - Listar candidatos")
        print("7 - Remover Candidato")
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

        elif op == "5":
            cadastrar_candidato()

        elif op == "6":
            listar_candidatos()

        elif op == "7":
            remover_candidato()

        elif op == "0":
            print("Voltando...")

        else:
            print("Opção inválida.")