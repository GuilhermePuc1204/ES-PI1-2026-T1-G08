# Importa o módulo random para gerar números aleatórios (usado para número de candidato)
import random

# Importa a conexão e o cursor do seu módulo de conexão com o banco
# conexao: objeto que representa a conexão com o MySQL
# cursor: objeto usado para executar comandos SQL
from database.conexao import conexao, cursor

def gerar_numero_candidato():
    """
    Gera um número único para o candidato.
    Utiliza números aleatórios entre 1000 e 9999 para garantir unicidade.
    """
    return random.randint(1000, 9999)

def cadastrar_candidato():
    """
    Cadastra um novo candidato no sistema.
    Solicita: nome, número de votação e partido.
    Valida a duplicidade de números antes de inserir.
    """
    print("\n=== CADASTRO DE CANDIDATO ===") # mostra o título da tela de cadastro

    nome = input("Nome completo: ")  # lê o nome do candidato
    numero = input("Número de votação: ")  # lê o número de votação do candidato
    partido = input("Partido: ")  # lê o partido do candidato

    # Verifica duplicidade de número
    sql = "SELECT * FROM candidatos WHERE numero_votacao = %s"  # comando SQL para verificar se já existe candidato com esse número
    cursor.execute(sql, (numero,))  # executa o SELECT passando o número como parâmetro

    if cursor.fetchone(): # se encontrou algum registro (já existe candidato com esse número)
        print("Número de votação já cadastrado.") # avisa que o número já está em uso
        return # sai da função sem cadastrar

    # ERRO 1 CORRIGIDO: Quebra de linha apropriada
    sql = ( # comando SQL para inserir um novo candidato
        "INSERT INTO candidatos (nome, numero_votacao, partido) "
        "VALUES (%s, %s, %s)"
    )

    cursor.execute(sql, (nome, numero, partido)) # executa o INSERT com os valores informados
    conexao.commit() # confirma a inserção no banco de dados

    print("\nCandidato cadastrado com sucesso!") # mensagem de sucesso
    print(f"Nome: {nome}") # exibe o nome cadastrado
    print(f"Número: {numero}")  # exibe o número cadastrado
    print(f"Partido: {partido}") # exibe o partido cadastrado 


def listar_candidatos():
    """
    Lista todos os candidatos cadastrados no sistema.
    Exibe: nome, número de votação e partido.
    """
    print("\n=== LISTA DE CANDIDATOS ===") # mostra o título da listagem

    sql = "SELECT nome, numero_votacao, partido FROM candidatos" # comando SQL para buscar os candidatos
    cursor.execute(sql) # executa o SELECT

    dados = cursor.fetchall() # busca todos os registros retornados

    if not dados: # se não houver registros
        print("Nenhum candidato cadastrado.") # avisa que a lista está vazia
        return # sai da função

    
    for c in dados:  # percorre cada candidato retornado
            print("\n------------------")  # separador visual
            print("Nome:", c[0])  # imprime o nome (primeira coluna)
            print("Número:", c[1])  # imprime o número de votação (segunda coluna)
            print("Partido:", c[2])  # imprime o partido (terceira coluna)



def buscar_candidato():
    """
    Busca um candidato específico pelo número de votação.
    Exibe os dados do candidato encontrado.
    """
    print("\n=== BUSCAR CANDIDATO ===") # mostra o título da busca

    numero = input("Número de votação: ") # lê o número a ser buscado

    # ERRO 2 CORRIGIDO: Quebra de linha apropriada
    sql = ( # comando SQL para buscar um candidato pelo número
        "SELECT nome, numero_votacao, partido "
        "FROM candidatos "
        "WHERE numero_votacao = %s"
    )

    cursor.execute(sql, (numero,)) # executa o SELECT passando o número como parâmetro
    c = cursor.fetchone() # busca o primeiro resultado encontrado

    if not c: # se não encontrou nenhum candidato
        print("Candidato não encontrado.")  # avisa que não existe
        return # sai da função

    
    print("\n=== ENCONTRADO ===")  # título de encontrado
    print("Nome:", c[0])  # imprime o nome
    print("Número:", c[1])  # imprime o número de votação
    print("Partido:", c[2])  # imprime o partido



def editar_candidato():
    """
    Edita as informações de um candidato existente.
    Permite alterar nome e partido, mantendo o número único.
    Valida a unicidade do novo número antes de atualizar.
    """
    
    print("\n=== EDITAR CANDIDATO ===")  # mostra o título da edição

    numero_atual = input("Número do candidato a editar: ")  # lê o número atual do candidato que será editado

    sql = "SELECT * FROM candidatos WHERE numero_votacao = %s"  # comando SQL para verificar se o candidato existe
    cursor.execute(sql, (numero_atual,))  # executa o SELECT passando o número atual


    if not cursor.fetchone(): # se não encontrou candidato com esse número
        print("Candidato não encontrado.") # avisa que não existe
        return #sai da função

    print("\nDigite os novos dados (deixe em branco para manter):") # instrução para o usuário

    nome = input("Novo nome: ")  # lê o novo nome (ou vazio para manter)
    numero_novo = input("Novo número: ")  # lê o novo número (ou vazio para manter)
    partido = input("Novo partido: ")  # lê o novo partido (ou vazio para manter)


    # Se o número foi alterado, verifica duplicidade
    if numero_novo and numero_novo != numero_atual: # se foi informado novo número e ele é diferente do atual
        sql = "SELECT * FROM candidatos WHERE numero_votacao = %s" # comando SQL para verificar se o novo número já existe
        cursor.execute(sql, (numero_novo,)) # executa o SELECT para o novo número
 
        if cursor.fetchone(): # se encontrou alguém com o novo número
            print("Novo número já está cadastrado.") # avisa duplicidade
            return # sai da função

    # Constrói a query dinamicamente com base no que foi alterado
    campos = [] # lista com os campos que serão atualizados
    valores = [] # lista com os valores correspondentes aos campos

    if nome: # se o usuário informou um novo nome
        campos.append("nome = %s") # adiciona o campo nome para atualização
        valores.append(nome) # adiciona o valor do novo nome

    if numero_novo: # se o usuário informou um novo número
        campos.append("numero_votacao = %s") # adiciona o campo numero_votacao para atualização
        valores.append(numero_novo) # adiciona o valor do novo número

    if partido: # se o usuário informou um novo partido
        campos.append("partido = %s") # adiciona o campo partido para atualização
        valores.append(partido) # adiciona o valor do novo partido
 
    if not campos: # se nada foi preenchido para alterar
        print("Nenhuma alteração foi feita.") # informa que não houve mudanças
        return # sai da função

    valores.append(numero_atual) # adiciona o número atual ao final para usar no WHERE

    sql = f"UPDATE candidatos SET {', '.join(campos)} WHERE numero_votacao = %s" # monta o UPDATE com os campos preenchidos

    cursor.execute(sql, valores) # executa o UPDATE com os valores na ordem correta
    conexao.commit() # confirma a atualização no banco
 
    print("Candidato atualizado com sucesso!") # mensagem de sucesso


def remover_candidato():
    """
    Remove um candidato do sistema.
    Solicita confirmação antes de deletar.
    """
    print("\n=== REMOVER CANDIDATO ===")  # mostra o título da remoção

    numero = input("Número do candidato: ") # lê o número do candidato a ser removido

    sql = "SELECT * FROM candidatos WHERE numero_votacao = %s" # comando SQL para verificar se o candidato existe
    cursor.execute(sql, (numero,)) # executa o SELECT passando o número

    if not cursor.fetchone(): # se não encontrou candidato
        print("Candidato não encontrado.") # avisa que não existe
        return # sai da função

    confirm = input("Confirmar remoção? (s/n): ") # pede confirmação antes de remover

    if confirm != "s": # se não confirmar com "s"
        return # cancela a remoção

    sql = "DELETE FROM candidatos WHERE numero_votacao = %s" # comando SQL para deletar o candidato pelo número
    cursor.execute(sql, (numero,)) # executa o DELETE passando o número
    conexao.commit() # confirma a remoção no banco

    print("Removido com sucesso.") # mensagem de sucesso