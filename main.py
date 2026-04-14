from gerenciamento.menu_gerenciamento import menu_gerenciamento  # importa a função do menu de gerenciamento


def main():  # função principal do sistema
    op=1
    while (op != 0):  # loop infinito para manter o sistema em execução
        print("\n=== SISTEMA DE VOTACAO ===")  # título do sistema
        print("1 - Gerenciamento")           # opção para acessar o gerenciamento
        print("2 - Votacao")                 # opção para acessar a votação
        print("0 - Sair")                    # opção para encerrar o sistema

        op = input("Escolha: ")  # lê a opção escolhida pelo usuário

        if op == "1":  # se a opção for 1
            menu_gerenciamento()  # chama o menu de gerenciamento

        elif op == "2":  # se a opção for 2
            print("\nMódulo de votação ainda não implementado.")  # informa que a votação não foi implementada

        elif op == "0":  # se a opção for 0
            print("Saindo...")  # mensagem de saída
            break
        else:  # se a opção for inválida
            print("Opção inválida.")  # informa erro de opção


if __name__ == "__main__":  # verifica se o arquivo está sendo executado diretamente
    main()  # chama a função principal