 Sistema de Votação Digital - Backend 

Projeto Integrador I – Engenharia de Software 
Pontifícia Universidade Católica de Campinas (PUC Campinas) 

 

Descrição do Projeto 

Sistema de votação digital desenvolvido em linha de comando para fins exclusivamente didáticos. O projeto integra conhecimentos em programação Python, manipulação de banco de dados MySQL e conceitos matemáticos de criptografia (Cifra de Hill). 

Este modelo é uma simulação acadêmica e não possui relação com o funcionamento, as tecnologias ou os sistemas de votação utilizados em processos eleitorais reais. 

Objetivo principal 

Desenvolver um backend robusto e seguro que implemente: 

Gerenciamento de eleitores e candidatos 

Processo de votação completo (abertura, votação, encerramento) 

Auditoria com logs de eventos críticos 

Resultados com múltiplas visualizações e validação de integridade 

Segurança através de criptografia e validação de dados 

 

Integrantes do Projeto 

Felipe Oliveira Barbosa  26001377

Fernando Munhoz Molinari  26000061

Guilherme Henrique Lopes Zambuzi  26003006

Murilo Henrique Giaretta Apolinario  22002255

Nathan Kenzo Puzipe 26002229

️ Tecnologias Utilizadas 

Linguagens e Frameworks 

Python 3.x – Linguagem principal de desenvolvimento 

MySQL – Sistema de gerenciamento de banco de dados 

 

 Bibliotecas em Python 

mysql-connector-python: Para conexão com banco de dados MySQL. 

datetime: Para manipulação de data e hora. 

random: Para geração de valores aleatórios. 

time: Para operações de tempo. 

os: Para operações do sistema operacional. 

Ferramentas de Desenvolvimento 

IDE: VSCode  

Versionamento: Git/GitHub 

Gerenciamento: GitHub Projects 

Banco de Dados: MySQL 8.0+ 

 

 Requisitos do Sistema 

Requisitos Funcionais Principais 

O sistema deve permitir o RF001 – Gerenciamento completo de eleitores e candidatos. Isso inclui o cadastro de eleitores com nome, título de eleitor, CPF e indicação de mesário, além da validação matemática de CPF e Título de Eleitor para prevenir duplicidade de dados. O sistema também deve gerar uma chave de acesso única para cada eleitor, e permitir a edição e remoção, bem como a busca e listagem de eleitores. O gerenciamento de candidatos (RF001.09 a RF001.14) é uma funcionalidade opcional que permite o cadastro, edição, remoção, busca e listagem de candidatos. 

O RF002 – Módulo de Votação deve processar o processo eleitoral em suas etapas. A Abertura do Sistema requer autenticação do mesário (título de eleitor + 4 primeiros dígitos do CPF + chave de acesso) e a execução do processo de Zerézima para limpar votos anteriores, listando os candidatos com votos zerados. Durante a Votação, o sistema deve identificar o eleitor, verificar se já votou, permitir a seleção de um candidato com confirmação, gerar um protocolo de votação e atualizar o status do eleitor. O Encerramento da votação exige validação do mesário, uma confirmação dupla (chave de acesso inserida duas vezes) e a consolidação dos resultados. 

O RF002.03 – Módulo de Resultados deve gerar o Boletim de Urna, exibindo os votos por candidato em ordem alfabética, além de estatísticas de comparecimento, mostrando a quantidade e o percentual de votantes. Também deve apresentar a somatória de votos por partido e realizar a validação de integridade, comparando os votos registrados com o número de eleitores que votaram. 

Para fins de auditoria, o RF002.02 – Módulo de Auditoria deve manter Logs de Ocorrências em um arquivo .txt, registrando eventos críticos como abertura e encerramento da votação, tentativas de acesso negadas e cada voto registrado. Além disso, deve ser possível listar todos os protocolos de votação gerados. 

Requisitos Não Funcionais 

RNF001 – O sistema deve ser desenvolvido utilizando a linguagem de programação Python 3.x, garantindo compatibilidade com versões modernas e acesso a bibliotecas atualizadas. 
RNF002 – Para o armazenamento persistente e seguro dos dados de eleitores, candidatos e votos, o sistema deve utilizar o banco de dados MySQL. 
RNF003 – A integração entre o Python e o MySQL será realizada através da biblioteca mysql.connector, assegurando uma comunicação eficiente e robusta com o banco de dados. 
RNF004 – A biblioteca datetime deve ser empregada para capturar e manipular informações de data e hora do sistema, essencial para registros de logs e timestamps de votação. 
RNF005 – Adicionalmente, as bibliotecas random, time e os podem ser utilizadas conforme a necessidade para funcionalidades como geração de números aleatórios, controle de tempo e interação com o sistema operacional, respectivamente. 
RNF006 – Um requisito crucial de segurança é a criptografia do CPF do eleitor, da chave de acesso e do protocolo de votação. Para isso, o sistema deve implementar o método de Cifra de Hill, garantindo a confidencialidade e integridade dessas informações sensíveis. 

 

 Como Executar o Projeto 

1️⃣ Pré-requisitos 

Antes de iniciar, certifique-se de ter instalado: 

Python 3.+ versão python  

MySQL Server 8.0+ mysql --version  

pip (gerenciador de pacotes Python) pip --version  

2️⃣ Instalação de Dependências 

Clone o repositório e instale as dependências: 

# Clone o repositório git clone https://github.com/GuilhermePuc1204/ES-PI1-2026-T1-G08.git
# Crie um ambiente virtual (recomendado) python -m venv venv 
# Ative o ambiente virtual 
# Instale as dependências pip install -r requirements.txt 

3️⃣ Configuração do Banco de Dados 

Opção A: Criar manualmente 

# Acesse o MySQL mysql -u root -p  # Execute os comandos SQL CREATE DATABASE votacao_sistema; USE votacao_sistema;  # Crie as tabelas (veja schema.sql) source schema.sql; 

Opção B: Usar script de inicialização 

Python setup_database.py 

4️⃣ Configuração de Conexão 

Edite o arquivo database/conexao.py com suas credenciais: 

conexao = mysql.connector.connect( host="localhost", user="seu_usuario", password="sua_senha", banco de dados="votacao_sistema" ) 

5️⃣ Executar o Sistema 

Python main.py 

O sistema iniciará com um menu interativo no terminal.  

 Exemplo de Uso 

Diretor do Cardápio 

=== SISTEMA DE VOTAÇÃO DIGITAL ===  1. Gerenciamento de Eleitores 2. Gerenciamento de Candidatos 3. Votação 4. Auditoria 5. Resultados 0. Sair  Escolha uma opção: _ 

Fluxo de Votação Típico 

Mesário abre o sistema → Autenticação → Zerézima 

Eleitor vota → Identificação → Seleção → Confirmação → Protocolo 

Mesário encerra → Dupla confirmação → Consolidação de resultados 

Visualizar resultados → Boletim, Estatísticas, Integridade 

 

 Segurança 

Validações Implementadas 

✅ Validação de CPF – Algoritmo matemático de dígitos verificadores 

✅ Validação de Título de Eleitor – Cálculo de dígitos verificadores 

✅ Prevenção de duplicidade – Verificação de CPF e Título únicos 

✅ Chave de acesso – Gerada automaticamente e criptografada 

✅ Voto duplo – Sistema impede que eleitor vote duas vezes 

✅ Logs de auditoria – Registro de todas as ações críticas 

Criptografia 

O sistema implementa Cifra de Hill para criptografar: 

CPF do eleitor 

Chave de acesso 

Protocolo de votação 

Veja utils/criptografia.py para detalhes técnicos. 

 

 Testes 

Executar testes unitários 

python -m testes pytest/ 

Teste manual de fluxo completo 

Cadastre 3 eleitores (1 mesário, 2 eleitores comuns) 

Cadastre 2 candidatos 

Abra votação como mesário 

Vote como eleitor comum 

Encerre votação 

Visualize resultados 



 Solução de problemas 

Erro: "ModuleNotFoundError: Nenhum módulo chamado 'mysql'" 

pip instalar mysql-connector-python 

Erro: "Não é possível conectar ao servidor MySQL" 

Verifique se o MySQL está rolando 

Confirme credenciais em database/conexao.py 

Verifique se o banco de dados foi criado 

Erro: "CPF ou Título inválido" 

Certifique-se de usar números reais 

Verifique os dígitos verificadores (Anexo A e B do requisito) 


 Licença 

Este projeto é desenvolvido para fins acadêmicos exclusivamente. 
 

Última atualização: 15 de abril de 2026 
 
