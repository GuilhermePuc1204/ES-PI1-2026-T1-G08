from votacao.votar import votar
from votacao.encerramento import encerrar_votacao


def menu_urna():
    """
    Exibe o menu de operação da urna após a abertura do sistema.

    Disponibilizado somente após a conclusão da Zerésima (RF002.01.06).
    Oferece as opções de registrar um voto ou encerrar a votação.

    Args:
        Nenhum.

    Returns:
        None
    """
    op = ""

    while True:
        print("\n=== URNA ELETRÔNICA ===")
        print("1 - Votar")
        print("2 - Encerrar Votação")

        op = input("Escolha: ").strip()

        if op == "1":
            # Inicia o fluxo de identificação e votação do eleitor
            votar()

        elif op == "2":
            # Inicia o fluxo de encerramento com autenticação do mesário
            encerrado = encerrar_votacao()
            if encerrado:
                # Só sai do loop se o encerramento foi confirmado e bem-sucedido
                break

        else:
            print("Opção inválida.")