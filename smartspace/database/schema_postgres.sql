-- =====================================================================
-- SmartSpace - Reserva de Espaços Compartilhados
-- Script DDL - PostgreSQL
-- ExpoTech 2026.2 - Missão 2050 - Categoria ARCHITECTURE (ADS 3º semestre)
-- =====================================================================

-- ---------------------------------------------------------------------
-- Tabela: USUARIO
-- ---------------------------------------------------------------------
CREATE TABLE usuario (
    id_usuario      SERIAL PRIMARY KEY,
    nome            VARCHAR(100) NOT NULL,
    email           VARCHAR(150) NOT NULL UNIQUE,
    senha_hash      VARCHAR(255) NOT NULL,
    tipo_usuario    VARCHAR(20)  NOT NULL,
    data_cadastro   TIMESTAMP    NOT NULL DEFAULT CURRENT_TIMESTAMP,
    ativo           BOOLEAN      NOT NULL DEFAULT TRUE,
    CONSTRAINT chk_tipo_usuario CHECK (tipo_usuario IN ('ADMIN', 'MORADOR'))
);

-- ---------------------------------------------------------------------
-- Tabela: ESPACO
-- ---------------------------------------------------------------------
CREATE TABLE espaco (
    id_espaco           SERIAL PRIMARY KEY,
    nome                VARCHAR(100) NOT NULL,
    descricao           VARCHAR(255),
    capacidade_maxima   INTEGER      NOT NULL,
    horario_abertura    TIME         NOT NULL,
    horario_fechamento  TIME         NOT NULL,
    ativo               BOOLEAN      NOT NULL DEFAULT TRUE,
    CONSTRAINT chk_capacidade CHECK (capacidade_maxima > 0),
    CONSTRAINT chk_horario_espaco CHECK (horario_fechamento > horario_abertura)
);

-- ---------------------------------------------------------------------
-- Tabela: RESERVA
-- ---------------------------------------------------------------------
CREATE TABLE reserva (
    id_reserva      SERIAL PRIMARY KEY,
    id_usuario      INTEGER      NOT NULL,
    id_espaco       INTEGER      NOT NULL,
    data_reserva    DATE         NOT NULL,
    hora_inicio     TIME         NOT NULL,
    hora_fim        TIME         NOT NULL,
    status          VARCHAR(20)  NOT NULL DEFAULT 'CONFIRMADA',
    data_criacao    TIMESTAMP    NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_reserva_usuario FOREIGN KEY (id_usuario) REFERENCES usuario(id_usuario),
    CONSTRAINT fk_reserva_espaco FOREIGN KEY (id_espaco) REFERENCES espaco(id_espaco),
    CONSTRAINT chk_horario_reserva CHECK (hora_fim > hora_inicio),
    CONSTRAINT chk_status_reserva CHECK (status IN ('CONFIRMADA', 'CANCELADA'))
);

-- ---------------------------------------------------------------------
-- Índices auxiliares (melhoram a checagem de conflito de horário)
-- ---------------------------------------------------------------------
CREATE INDEX idx_reserva_espaco_data ON reserva (id_espaco, data_reserva);
CREATE INDEX idx_reserva_usuario ON reserva (id_usuario);

-- ---------------------------------------------------------------------
-- Dados de exemplo (opcional, útil para testes durante o desenvolvimento)
-- ---------------------------------------------------------------------
INSERT INTO usuario (nome, email, senha_hash, tipo_usuario) VALUES
    ('Maria Síndica', 'maria.admin@smartspace.com', '<hash_da_senha>', 'ADMIN'),
    ('Enrico Morador', 'enrico@smartspace.com', '<hash_da_senha>', 'MORADOR');

INSERT INTO espaco (nome, descricao, capacidade_maxima, horario_abertura, horario_fechamento) VALUES
    ('Salão de Festas', 'Espaço para eventos e comemorações', 50, '08:00', '22:00'),
    ('Churrasqueira', 'Área externa com churrasqueira e mesas', 20, '10:00', '23:00');

-- Regra de conflito de horário (duas reservas não podem se sobrepor no
-- mesmo espaço/data) é validada na camada de aplicação (Python), no
-- método esta_disponivel() da classe Espaco, e não apenas via constraint
-- de banco, pois exige comparação lógica entre múltiplos registros.
