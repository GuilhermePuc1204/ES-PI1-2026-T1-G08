from votacao.abertura import abrir_votacao
from votacao.resultados import menu_resultados
from utils.auditoria import visualizar_auditoria

def menu_votacao():

    op = -1

    while op != "0":
        print("\n=== VOTAÇÃO ===")
        print("1 - Abrir Sistema de Votação")
        print("2 - Auditoria da Votação")
        print("3 - Resultados da Votação")
        print("0 - Voltar")

        op = input("Escolha: ")

        if op == "1":
            abrir_votacao()

        elif op == "2":
            visualizar_auditoria()

        elif op == "3":
            menu_resultados()

        elif op == "0":
            print("Voltando...")

        else:
            print("Opção inválida.")