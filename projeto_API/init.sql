-- Script de criação do banco (executado automaticamente pelo container do PostgreSQL
-- na PRIMEIRA subida do volume). Para recriar do zero: docker compose down -v

CREATE TABLE operador (
    id      SERIAL PRIMARY KEY,
    nome    VARCHAR(100) NOT NULL,
    perfil  VARCHAR(20)  NOT NULL CHECK (perfil IN ('OPERADOR', 'SUPERVISOR')),
    zona    VARCHAR(50)  NOT NULL
);

CREATE TABLE sensor (
    id                     SERIAL PRIMARY KEY,
    nome                   VARCHAR(100) NOT NULL,
    tipo                   VARCHAR(20)  NOT NULL CHECK (tipo IN ('TEMPERATURA', 'UMIDADE', 'PRESSAO')),
    zona                   VARCHAR(50)  NOT NULL,
    status                 VARCHAR(20)  NOT NULL DEFAULT 'NORMAL'
                           CHECK (status IN ('NORMAL', 'ALERTA_CRITICO', 'OFFLINE')),
    ativo                  BOOLEAN      NOT NULL DEFAULT TRUE,
    intervalo_segundos     INTEGER      NOT NULL DEFAULT 300 CHECK (intervalo_segundos > 0),
    limite_seguranca       DOUBLE PRECISION NOT NULL,
    instalado_em           TIMESTAMP    NOT NULL DEFAULT NOW(),
    ultima_comunicacao     TIMESTAMP,
    ultimo_valor           DOUBLE PRECISION,
    ultimo_valor_em        TIMESTAMP,
    leituras_acima_limite  INTEGER      NOT NULL DEFAULT 0,
    atuador_tipo           VARCHAR(20)  NOT NULL DEFAULT 'RELE' CHECK (atuador_tipo IN ('RELE', 'VALVULA')),
    atuador_estado         VARCHAR(20)  NOT NULL DEFAULT 'LIGADO'
);

CREATE TABLE leitura (
    id             SERIAL PRIMARY KEY,
    sensor_id      INTEGER NOT NULL REFERENCES sensor(id),
    valor          DOUBLE PRECISION NOT NULL,
    flag           VARCHAR(30) NOT NULL DEFAULT 'OK'
                   CHECK (flag IN ('OK', 'SUSPEITA_RUIDO', 'REQUER_CALIBRACAO')),
    agregada       BOOLEAN   NOT NULL DEFAULT FALSE,
    registrada_em  TIMESTAMP NOT NULL DEFAULT NOW()
);
CREATE INDEX idx_leitura_sensor_data ON leitura (sensor_id, registrada_em);

-- REGRA 8 também no banco: telemetria é imutável (defesa em profundidade)
CREATE FUNCTION bloquear_alteracao_leitura() RETURNS trigger AS $$
BEGIN
    RAISE EXCEPTION 'Leituras de telemetria são imutáveis (log auditável)';
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_leitura_imutavel
BEFORE UPDATE OR DELETE ON leitura
FOR EACH ROW EXECUTE FUNCTION bloquear_alteracao_leitura();

CREATE TABLE manutencao (
    id             SERIAL PRIMARY KEY,
    sensor_id      INTEGER NOT NULL REFERENCES sensor(id) ON DELETE CASCADE,
    data_afericao  TIMESTAMP NOT NULL DEFAULT NOW(),
    descricao      VARCHAR(255)
);

CREATE TABLE alerta (
    id               SERIAL PRIMARY KEY,
    sensor_id        INTEGER NOT NULL REFERENCES sensor(id) ON DELETE CASCADE,
    prioridade       VARCHAR(10) NOT NULL DEFAULT 'ALTA' CHECK (prioridade IN ('ALTA', 'MEDIA', 'BAIXA')),
    status           VARCHAR(20) NOT NULL DEFAULT 'ABERTO'
                     CHECK (status IN ('ABERTO', 'RECONHECIDO', 'ESCALONADO')),
    mensagem         VARCHAR(255),
    criado_em        TIMESTAMP NOT NULL DEFAULT NOW(),
    reconhecido_por  INTEGER REFERENCES operador(id),
    reconhecido_em   TIMESTAMP
);

-- ----------------------------------------------------------- dados iniciais
INSERT INTO operador (nome, perfil, zona) VALUES
    ('Carlos Supervisor', 'SUPERVISOR', 'ADMINISTRACAO'),   -- id 1
    ('Ana Operadora',     'OPERADOR',   'ZONA_A'),          -- id 2
    ('Bruno Operador',    'OPERADOR',   'ZONA_B');          -- id 3

INSERT INTO sensor (nome, tipo, zona, limite_seguranca, intervalo_segundos, atuador_tipo, atuador_estado) VALUES
    ('Temp Caldeira 01',  'TEMPERATURA', 'ZONA_A',  80, 300, 'RELE',    'LIGADO'),   -- id 1
    ('Umidade Estoque 01','UMIDADE',     'ZONA_A',  85, 300, 'RELE',    'LIGADO'),   -- id 2
    ('Temp Forno 02',     'TEMPERATURA', 'ZONA_B', 100, 300, 'VALVULA', 'ABERTA');   -- id 3

-- id 4: instalado há 200 dias e sem aferição -> demonstra REQUER_CALIBRACAO (regra 7)
INSERT INTO sensor (nome, tipo, zona, limite_seguranca, intervalo_segundos, instalado_em) VALUES
    ('Pressao Linha 03', 'PRESSAO', 'ZONA_B', 900, 300, NOW() - INTERVAL '200 days');

-- id 5: intervalo de 5 s -> fica OFFLINE em ~15 s sem dados (regra 4)
INSERT INTO sensor (nome, tipo, zona, limite_seguranca, intervalo_segundos) VALUES
    ('Temp Demo Watchdog', 'TEMPERATURA', 'ZONA_A', 80, 5);

-- o sensor 1 foi aferido há 10 dias (não precisa de calibração)
INSERT INTO manutencao (sensor_id, data_afericao, descricao) VALUES
    (1, NOW() - INTERVAL '10 days', 'Aferição periódica de rotina');
