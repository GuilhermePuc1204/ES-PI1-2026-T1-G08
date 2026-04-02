from gerenciamento.eleitores import (
    cadastrar_eleitor,  # importa a função responsável por cadastrar eleitores
    listar_eleitores,   # importa a função que lista todos os eleitores
    buscar_eleitor,     # importa a função que busca um eleitor específico
    remover_eleitor     # importa a função que remove um eleitor
)

op=1
def menu_gerenciamento():  # função que exibe e controla o menu de gerenciamento de eleitores

    while (op != 0):  # loop infinito para manter o menu ativo até o usuário sair
        print("\n=== GERENCIAMENTO ===")  # título do menu
        print("1 - Cadastrar eleitor")   # opção para cadastrar eleitor
        print("2 - Listar eleitores")    # opção para listar eleitores
        print("3 - Buscar eleitor")      # opção para buscar eleitor
        print("4 - Remover eleitor")     # opção para remover eleitor
        print("0 - Voltar")               # opção para sair do menu

        op = input("Escolha: ")  # lê a opção escolhida pelo usuário

        if op == "1":  # se a opção for 1
            cadastrar_eleitor()  # chama a função de cadastro de eleitor

        elif op == "2":  # se a opção for 2
            listar_eleitores()  # chama a função de listagem de eleitores

        elif op == "3":  # se a opção for 3
            buscar_eleitor()  # chama a função de busca de eleitor

        elif op == "4":  # se a opção for 4
            remover_eleitor()  # chama a função de remoção de eleitor

        elif op == "0":  # se a opção for 0
            print("Voltando...")  # Imprime a mensagem de retorno ao menu principal

        else:  # se a opção não for válida
            print("Opção inválida.")  # informa que a opção escolhida é inválida