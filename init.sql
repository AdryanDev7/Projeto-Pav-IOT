CREATE TABLE localizacoes (
    id SERIAL PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    setor VARCHAR(50) NOT NULL,
    latitude DECIMAL(10, 8) NOT NULL,
    longitude DECIMAL(11, 8) NOT NULL
);

CREATE TABLE sensores (
    id SERIAL PRIMARY KEY,
    codigo_serial VARCHAR(50) UNIQUE NOT NULL,
    tipo VARCHAR(50) NOT NULL,
    status VARCHAR(20) NOT NULL DEFAULT 'Ativo',
    localizacao_id INT REFERENCES localizacoes(id) ON DELETE RESTRICT,
    nivel_bateria INT NOT NULL  
);

CREATE TABLE leituras_sensores (
    id SERIAL PRIMARY KEY,
    sensor_id INT REFERENCES sensores(id) ON DELETE CASCADE,
    valor DECIMAL(10, 4) NOT NULL,
    nivel_bateria INT NOT NULL,
    data_hora TIMESTAMP NOT NULL
);

CREATE TABLE anomalias (
    id SERIAL PRIMARY KEY,
    leitura_id INT REFERENCES leituras_sensores(id) ON DELETE CASCADE,
    descricao_alerta TEXT NOT NULL,
    severidade VARCHAR(20) NOT NULL
);