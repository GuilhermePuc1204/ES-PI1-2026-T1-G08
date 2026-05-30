from utils.criptografia import alfabeto, alfabeto_chave


chave_hill_inversa = [
    [15, 17],
    [20, 9]
]

chave_hill_chave_inversa = [
    [31, 2],
    [3, 35]
]

def descriptografar_cpf(cpf_cifrado):
    """
    Descriptografa um CPF cifrado com a Cifra de Hill.

    Args:
        cpf_cifrado (str): CPF criptografado (A–Z).

    Returns:
        str: CPF original (apenas números).
    """

    valores = [alfabeto.index(c) for c in cpf_cifrado]

    resultado = []

    for i in range(0, len(valores), 2):
        x = valores[i]
        y = valores[i + 1]

        p1 = (chave_hill_inversa[0][0] * x + chave_hill_inversa[0][1] * y) % 26
        p2 = (chave_hill_inversa[1][0] * x + chave_hill_inversa[1][1] * y) % 26

        resultado.append(str(p1))
        resultado.append(str(p2))

    return "".join(resultado)


def descriptografar_protocolo(texto_cifrado):
    """
    Descriptografa um protocolo de votação cifrado com a Cifra de Hill.

    Aplica a matriz chave inversa sobre o alfabeto expandido (A-Z + 0-9),
    revertendo o processo de criptografia em blocos de 2 caracteres.
    Utilizado pela auditoria para exibir protocolos em texto claro
    para conferência.

    Args:
        texto_cifrado (str): Protocolo de votação criptografado.

    Returns:
        str: Protocolo original (texto claro).
    """
    valores = []

    for c in texto_cifrado:
        valores.append(alfabeto_chave.index(c))

    resultado = []

    for i in range(0, len(valores), 2):
        x = valores[i]
        y = valores[i + 1]

        p1 = (chave_hill_chave_inversa[0][0] * x +
              chave_hill_chave_inversa[0][1] * y) % len(alfabeto_chave)

        p2 = (chave_hill_chave_inversa[1][0] * x +
              chave_hill_chave_inversa[1][1] * y) % len(alfabeto_chave)

        resultado.append(alfabeto_chave[p1])
        resultado.append(alfabeto_chave[p2])

    return "".join(resultado)
