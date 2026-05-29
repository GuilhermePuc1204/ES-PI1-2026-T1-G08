alfabeto = [
    "A","B","C","D","E","F","G","H","I","J","K","L","M",
    "N","O","P","Q","R","S","T","U","V","W","X","Y","Z"
]

chave_hill = [
    [3, 3],
    [2, 5]
]

chave_hill_chave = [
    [1, 2],
    [3, 5]
]

alfabeto_chave = [
    "A","B","C","D","E","F","G","H","I","J","K","L","M",
    "N","O","P","Q","R","S","T","U","V","W","X","Y","Z",
    "0","1","2","3","4","5","6","7","8","9"
]

def criptografar_cpf(cpf):
    cpf = [int(d) for d in cpf]


    if len(cpf) % 2 != 0:
        cpf.append(0)

    resultado = []

    for i in range(0, len(cpf), 2):
        x = cpf[i]
        y = cpf[i + 1]

        r1 = (chave_hill[0][0] * x + chave_hill[0][1] * y) % len(alfabeto)
        r2 = (chave_hill[1][0] * x + chave_hill[1][1] * y) % len(alfabeto)


        resultado.append(alfabeto[r1])
        resultado.append(alfabeto[r2])

    return "".join(resultado)


# ==========================================================
# CRIPTOGRAFIA DA CHAVE DE ACESSO
# ==========================================================
def criptografar_chave_acesso(chave):
    """
    Criptografa a chave de acesso do eleitor utilizando a Cifra de Hill.

    Diferença em relação ao CPF:
    - A chave de acesso possui letras e números
    - Por isso, utiliza um alfabeto expandido (A-Z + 0-9)

    Args:
        chave (str): Chave de acesso em texto claro.

    Returns:
        str: Chave de acesso criptografada.
    """

    valores = []
    for c in chave.upper():
        if c not in alfabeto_chave:
            raise ValueError("Caractere inválido na chave de acesso")
        valores.append(alfabeto_chave.index(c))

    # Garante quantidade par de elementos
    if len(valores) % 2 != 0:
        valores.append(0)

    resultado = []

    # Processa a chave em blocos de 2
    for i in range(0, len(valores), 2):
        x = valores[i]
        y = valores[i + 1]

        # Aplicação da Cifra de Hill
        r1 = (chave_hill_chave[0][0] * x + chave_hill_chave[0][1] * y) % len(alfabeto_chave)
        r2 = (chave_hill_chave[1][0] * x + chave_hill_chave[1][1] * y) % len(alfabeto_chave)

        resultado.append(alfabeto_chave[r1])
        resultado.append(alfabeto_chave[r2])

    # Retorna a chave criptografada
    return "".join(resultado)

def criptografar_protocolo(protocolo):
    return criptografar_chave_acesso(protocolo)