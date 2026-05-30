# Sistema de Votação Digital — Backend

**Projeto Integrador I – Engenharia de Software**  
Pontifícia Universidade Católica de Campinas (PUC Campinas)

---

## Descrição do Projeto

Sistema de votação digital executado em linha de comando, desenvolvido para fins exclusivamente didáticos. O projeto integra conhecimentos em programação Python, manipulação de banco de dados MySQL e conceitos matemáticos de criptografia (Cifra de Hill).

> Este modelo é uma simulação acadêmica e não possui relação com o funcionamento, as tecnologias ou os sistemas de votação utilizados em processos eleitorais reais.

---

## Integrantes do Projeto

| Nome | RA |
|------|----|
| Felipe Oliveira Barbosa | 26001377 |
| Fernando Munhoz Molinari | 26000061 |
| Guilherme Henrique Lopes Zambuzi | 26003006 |
| Murilo Henrique Giaretta Apolinario | 22002255 |
| Nathan Kenzo Puzipe | 26002229 |

---

## Tecnologias Utilizadas

- **Linguagem:** Python 3.x
- **Banco de dados:** MySQL 8.0+
- **Bibliotecas Python:** `mysql-connector-python`, `datetime`, `random`, `os`
- **IDE:** VSCode
- **Versionamento:** Git / GitHub
- **Gerenciamento:** GitHub Projects

---

## Como Executar o Projeto

### Pré-requisitos

- Python 3.x instalado
- MySQL Server 8.0+ instalado e em execução

### 1. Clone o repositório

```bash
git clone https://github.com/GuilhermePuc1204/ES-PI1-2026-T1-G08.git
cd ES-PI1-2026-T1-G08
```

### 2. Instale a dependência

```bash
pip install mysql-connector-python
```

### 3. Configure o banco de dados

Acesse o MySQL e execute os comandos abaixo para criar o banco e as tabelas:

```bash
mysql -u root -p
```

```sql
CREATE DATABASE sistema_votacao;
USE sistema_votacao;
source database/script.sql;
```

> **Atenção:** se o MySQL estiver configurado sem senha para o usuário `root`, basta pressionar Enter quando solicitado.

### 4. Verifique as credenciais de conexão

Abra o arquivo `database/conexao.py` e confirme que as credenciais correspondem ao seu ambiente:

```python
conexao = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",          # ajuste se necessário
    database="sistema_votacao"
)
```

### 5. Execute o sistema

```bash
python main.py
```

O sistema iniciará com o menu principal no terminal:

```
=== SISTEMA DE VOTACAO ===
1 - Gerenciamento
2 - Votacao
0 - Sair
Escolha:
```

---

## Fluxo de Uso Típico

1. **Gerenciamento:** cadastre eleitores (ao menos um com perfil de mesário) e candidatos
2. **Votação → Abrir Sistema:** o mesário se autentica e a zerésima é executada
3. **Votação → Votar:** cada eleitor se identifica e registra seu voto
4. **Votação → Encerrar:** o mesário encerra com dupla confirmação de chave
5. **Votação → Resultados:** boletim de urna, comparecimento, votos por partido e validação de integridade
6. **Votação → Auditoria:** logs de ocorrências e protocolos de votação

---

## Segurança

- **Validação de CPF** — cálculo matemático dos dígitos verificadores
- **Validação de Título de Eleitor** — cálculo matemático dos dígitos verificadores
- **Prevenção de duplicidade** — CPF e Título únicos no banco de dados
- **Chave de acesso** — gerada automaticamente e armazenada criptografada
- **Prevenção de voto duplo** — status `JA_VOTOU` verificado antes de cada voto
- **Logs de auditoria** — registro em arquivo `.txt` de todos os eventos críticos
- **Criptografia (Cifra de Hill)** — CPF, chave de acesso e protocolo de votação são criptografados antes de serem salvos no banco

---

## Solução de Problemas

**`ModuleNotFoundError: No module named 'mysql'`**
```bash
pip install mysql-connector-python
```

**`Can't connect to MySQL server`**
- Verifique se o MySQL está em execução
- Confirme as credenciais em `database/conexao.py`
- Verifique se o banco `sistema_votacao` foi criado

**`CPF ou Título inválido`**
- Utilize números reais com dígitos verificadores válidos

---

## Estrutura do Projeto

```
ES-PI1-2026-T1-G08/
├── main.py
├── database/
│   ├── conexao.py
│   └── script.sql
├── gerenciamento/
│   ├── candidatos.py
│   ├── eleitores.py
│   └── menu_gerenciamento.py
├── votacao/
│   ├── abertura.py
│   ├── encerramento.py
│   ├── resultados.py
│   ├── urna.py
│   ├── votar.py
│   └── menu_votacao.py
└── utils/
    ├── auditoria.py
    ├── criptografia.py
    ├── descriptografia.py
    └── validacoes.py
```

---

*Projeto acadêmico — PUC Campinas, 2026*
