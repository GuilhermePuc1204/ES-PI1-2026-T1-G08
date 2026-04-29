USE sistema_votacao;

CREATE TABLE IF NOT EXISTS candidatos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(150) NOT NULL,
    numero INT UNIQUE NOT NULL,
    partido VARCHAR(50) NOT NULL
);

CREATE TABLE IF NOT EXISTS votos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    id_eleitor INT,
    id_candidato INT,
    data_hora DATETIME,
    protocolo VARCHAR(100),

    FOREIGN KEY (id_eleitor) REFERENCES eleitores(id),
    FOREIGN KEY (id_candidato) REFERENCES candidatos(id)
);

CREATE TABLE IF NOT EXISTS urna (
    id INT AUTO_INCREMENT PRIMARY KEY,
    status VARCHAR(20),
    data_abertura DATETIME,
    data_encerramento DATETIME
);

CREATE TABLE IF NOT EXISTS logs (
    id INT AUTO_INCREMENT PRIMARY KEY,
    data_hora DATETIME,
    evento VARCHAR(255)
);

CREATE TABLE IF NOT EXISTS protocolos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    codigo VARCHAR(100),
    data_hora DATETIME
);

CREATE TABLE IF NOT EXISTS resultados (
    id INT AUTO_INCREMENT PRIMARY KEY,
    id_candidato INT,
    total_votos INT,
    FOREIGN KEY (id_candidato) REFERENCES candidatos(id)
);