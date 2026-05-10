CREATE TABLE IF NOT EXISTS eleitores (
    id SERIAL PRIMARY KEY,
    nome VARCHAR(150) NOT NULL,
    cpf VARCHAR(50) NOT NULL UNIQUE,
    titulo_eleitor VARCHAR(12) NOT NULL UNIQUE,
    mesario BOOLEAN NOT NULL,
    chave_acesso VARCHAR(50) NOT NULL,
    status_voto VARCHAR(20) DEFAULT 'Não votou'
);

CREATE TABLE IF NOT EXISTS candidatos (
    id SERIAL PRIMARY KEY,
    nome VARCHAR(150) NOT NULL,
    numero INT NOT NULL UNIQUE,
    partido VARCHAR(50) NOT NULL
);

CREATE TABLE IF NOT EXISTS votos (
    id SERIAL PRIMARY KEY,
    id_candidato INT NOT NULL,
    data_hora TIMESTAMP NOT NULL,
    protocolo VARCHAR(100) NOT NULL,
    FOREIGN KEY (id_candidato) REFERENCES candidatos(id)
);

