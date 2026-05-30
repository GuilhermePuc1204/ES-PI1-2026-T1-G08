from gerenciamento.menu_gerenciamento import menu_gerenciamento  # importa a função do menu de gerenciamento
from votacao.menu_votacao import menu_votacao  # importa a função do menu de votação

def main():
    """
    Função principal do sistema de votação.

    Exibe o menu inicial em loop, permitindo o acesso ao módulo de
    Gerenciamento (cadastros) ou ao módulo de Votação (urna, auditoria
    e resultados), até que o usuário escolha sair.

    Args:
        Nenhum.

    Returns:
        None: A função não retorna valor; encerra ao sair do loop.
    """
    op=1
    while (op != 0):  # loop infinito para manter o sistema em execução
        print("\n=== SISTEMA DE VOTACAO ===") 
        print("1 - Gerenciamento")           # opção para acessar o gerenciamento
        print("2 - Votacao")                 # opção para acessar a votação
        print("0 - Sair")                    # opção para encerrar o sistema

        op = input("Escolha: ")  # lê a opção escolhida pelo usuário

        if op == "1":  # se a opção for 1
            menu_gerenciamento()  # chama o menu de gerenciamento

        elif op == "2":  # se a opção for 2
            menu_votacao()  # chama o menu de votação

        elif op == "0":  # se a opção for 0
            print("Saindo...")  
            break
        else:  # se a opção for inválida
            print("Opção inválida.")  

if __name__ == "__main__":  # verifica se o arquivo está sendo executado diretamente
    main()  # chama a função principal