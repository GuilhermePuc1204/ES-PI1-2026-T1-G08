from votacao.votar import votar
from utils.auditoria import registrar_evento
from votacao.encerramento import encerrar_votacao

def menu_urna():

    op =""

    while op != "0":
        print("\n=== URNA ELETRÔNICA ===")
        print("1 - Votar")
        print("2 - Encerrar Votação")
        print("0 - Voltar")

        op = input("Escolha: ")

        if op == "1":
            votar()

        elif op == "2":
            if encerrar_votacao():
                # encerramento confirmado: sai da urna e volta ao menu de votação
                break

        elif op == "0":
            print("Voltando...")

        else:
            print("Opção inválida.")