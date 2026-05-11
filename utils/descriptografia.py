from utils.criptografia import alfabeto 


# Matriz inversa da chave de Hill (mod 26)
chave_hill_inversa = [
    [15, 17],
    [20, 9]
]

def descriptografar_cpf(cpf_cifrado):
    """
    Descriptografa um CPF cifrado com a Cifra de Hill.

    Args:
        cpf_cifrado (str): CPF criptografado (A–Z).

    Returns:
        str: CPF original (apenas números).
    """

    # Converte letras para índices
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