# ==========================================================
# DEFINIÇÃO DOS ALFABETOS E MATRIZ-CHAVE
# ==========================================================

# Alfabeto utilizado para criptografia do CPF
# Contém apenas letras, pois o CPF é composto exclusivamente por números
alfabeto = [
    "A","B","C","D","E","F","G","H","I","J","K","L","M",
    "N","O","P","Q","R","S","T","U","V","W","X","Y","Z"
]

# Matriz-chave da Cifra de Hill (2x2)
# Esta matriz é fixa e conhecida pelo sistema
# Seu uso permite a transformação linear dos dados
chave_hill = [
    [3, 3],
    [2, 5]
]

# Alfabeto utilizado para criptografia da chave de acesso
# Inclui letras e números, pois a chave de acesso possui ambos
alfabeto_chave = [
    "A","B","C","D","E","F","G","H","I","J","K","L","M",
    "N","O","P","Q","R","S","T","U","V","W","X","Y","Z",
    "0","1","2","3","4","5","6","7","8","9"
]


# ==========================================================
# CRIPTOGRAFIA DO CPF
# ==========================================================
def criptografar_cpf(cpf):
    """
    Criptografa o CPF do eleitor utilizando a Cifra de Hill (matriz 2x2).

    Processo aplicado:
    1. Conversão dos dígitos do CPF para inteiros
    2. Agrupamento dos dados em pares
    3. Multiplicação pela matriz-chave
    4. Aplicação de módulo para limitar o domínio
    5. Conversão do resultado para letras

    Args:
        cpf (str): CPF válido contendo apenas números.

    Returns:
        str: CPF criptografado em formato alfabético.
    """

    # Remove pontos, traços e qualquer caractere não numérico antes de processar
    cpf = ''.join(c for c in cpf if c.isdigit())

    # Converte cada dígito do CPF para inteiro
    cpf = [int(d) for d in cpf]

    # Garante que a quantidade de elementos seja par
    # A Cifra de Hill trabalha com blocos compatíveis com a matriz (2x2)
    if len(cpf) % 2 != 0:
        cpf.append(0)

    resultado = []

    # Processa o CPF em blocos de 2 valores
    for i in range(0, len(cpf), 2):
        x = cpf[i]
        y = cpf[i + 1]

        # Aplicação da Cifra de Hill:
        # Multiplicação da matriz-chave pelo vetor [x, y]
        r1 = (chave_hill[0][0] * x + chave_hill[0][1] * y) % len(alfabeto)
        r2 = (chave_hill[1][0] * x + chave_hill[1][1] * y) % len(alfabeto)

        # Conversão dos valores numéricos para letras
        resultado.append(alfabeto[r1])
        resultado.append(alfabeto[r2])

    # Retorna o CPF criptografado como string
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

    # Converte cada caractere da chave em um índice do alfabeto
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
        r1 = (chave_hill[0][0] * x + chave_hill[0][1] * y) % len(alfabeto_chave)
        r2 = (chave_hill[1][0] * x + chave_hill[1][1] * y) % len(alfabeto_chave)

        resultado.append(alfabeto_chave[r1])
        resultado.append(alfabeto_chave[r2])

    # Retorna a chave criptografada
    return "".join(resultado)