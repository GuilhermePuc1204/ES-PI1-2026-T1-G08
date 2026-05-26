from gerenciamento.candidatos import (cadastrar_candidato, listar_candidatos, remover_candidato, buscar_candidato)
from gerenciamento.eleitores import (cadastrar_eleitor, listar_eleitores, buscar_eleitor, remover_eleitor, editar_eleitor)

def menu_gerenciamento():

    op = -1  # inicializa a variável

    while op != "0":
        print("\n=== GERENCIAMENTO ===")
        print("1 - Cadastrar eleitor")
        print("2 - Listar eleitores")
        print("3 - Buscar eleitor")
        print("4 - Editar eleitor")
        print("5 - Remover eleitor")
        print("6 - Cadastrar candidato")
        print("7 - Listar candidatos")
        print("8 - Remover Candidato")
        print("9 - Buscar Candidato")
        print("0 - Voltar")

        op = input("Escolha: ")

        if op == "1":
            cadastrar_eleitor()

        elif op == "2":
            listar_eleitores()

        elif op == "3":
            buscar_eleitor()

        elif op == "4":
            editar_eleitor()

        elif op == "5":
            remover_eleitor()

        elif op == "6":
            cadastrar_candidato()

        elif op == "7":
            listar_candidatos()

        elif op == "8":
            remover_candidato()

        elif op == "9":
            buscar_candidato()

        elif op == "0":
            print("Voltando...")

        else:
            print("Opção inválida.")