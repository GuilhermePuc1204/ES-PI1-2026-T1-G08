from votacao.votar import votar
from utils.auditoria import registrar_evento
from votacao.encerramento import encerrar_votacao

def menu_urna():
    """
    Exibe o menu de operação da urna eletrônica após a abertura do sistema.

    Apresenta em loop as opções "Votar" (registra um novo voto) e
    "Encerrar Votação" (com dupla confirmação do mesário). Sai do loop
    automaticamente quando o encerramento é confirmado com sucesso.

    Args:
        Nenhum.

    Returns:
        None: A função não retorna valor; encerra ao sair do loop ou ao
        encerrar a votação.
    """
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