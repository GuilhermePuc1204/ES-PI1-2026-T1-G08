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

    while op != "2":
        print("\n=== URNA ELETRÔNICA ===")
        print("1 - Votar")
        print("2 - Encerrar Votação")

        op = input("Escolha: ").strip()

        if op == "1":
            # Inicia o fluxo de identificação e votação do eleitor
            votar()

        elif op == "2":
            # Só sai do loop se o encerramento for confirmado com sucesso
            # Se o mesário cancelar, reseta op para continuar o loop
            if not encerrar_votacao():
                op = ""

        else:
            print("Opção inválida.")
            op = ""