CREATE DATABASE IF NOT EXISTS smartspace
    CHARACTER SET utf8mb4
    COLLATE utf8mb4_unicode_ci;

USE smartspace;

CREATE TABLE IF NOT EXISTS usuario (
    id_usuario     INT AUTO_INCREMENT PRIMARY KEY,
    nome           VARCHAR(100) NOT NULL,
    email          VARCHAR(150) NOT NULL UNIQUE,
    senha_hash     VARCHAR(255) NOT NULL,
    tipo_usuario   VARCHAR(20)  NOT NULL,
    data_cadastro  TIMESTAMP    NOT NULL DEFAULT CURRENT_TIMESTAMP,
    ativo          BOOLEAN      NOT NULL DEFAULT TRUE,
    CONSTRAINT chk_tipo_usuario CHECK (tipo_usuario IN ('ADMIN', 'MORADOR'))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS espaco (
    id_espaco           INT AUTO_INCREMENT PRIMARY KEY,
    nome                VARCHAR(100) NOT NULL,
    descricao           VARCHAR(255),
    capacidade_maxima   INT          NOT NULL,
    horario_abertura    TIME         NOT NULL,
    horario_fechamento  TIME         NOT NULL,
    ativo               BOOLEAN      NOT NULL DEFAULT TRUE,
    CONSTRAINT chk_capacidade CHECK (capacidade_maxima > 0),
    CONSTRAINT chk_horario_espaco CHECK (horario_fechamento > horario_abertura)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS reserva (
    id_reserva    INT AUTO_INCREMENT PRIMARY KEY,
    id_usuario    INT         NOT NULL,
    id_espaco     INT         NOT NULL,
    data_reserva  DATE        NOT NULL,
    hora_inicio   TIME        NOT NULL,
    hora_fim      TIME        NOT NULL,
    status        VARCHAR(20) NOT NULL DEFAULT 'CONFIRMADA',
    data_criacao  TIMESTAMP   NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_reserva_usuario FOREIGN KEY (id_usuario) REFERENCES usuario (id_usuario),
    CONSTRAINT fk_reserva_espaco FOREIGN KEY (id_espaco) REFERENCES espaco (id_espaco),
    CONSTRAINT chk_horario_reserva CHECK (hora_fim > hora_inicio),
    CONSTRAINT chk_status_reserva CHECK (status IN ('CONFIRMADA', 'CANCELADA')),
    INDEX idx_reserva_espaco_data (id_espaco, data_reserva),
    INDEX idx_reserva_usuario (id_usuario)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

INSERT INTO espaco (nome, descricao, capacidade_maxima, horario_abertura, horario_fechamento)
SELECT 'Salão de Festas', 'Espaço para eventos e comemorações', 50, '08:00', '22:00'
FROM DUAL
WHERE NOT EXISTS (SELECT 1 FROM espaco WHERE nome = 'Salão de Festas');

INSERT INTO espaco (nome, descricao, capacidade_maxima, horario_abertura, horario_fechamento)
SELECT 'Churrasqueira', 'Área externa com churrasqueira e mesas', 20, '08:00', '22:00'
FROM DUAL
WHERE NOT EXISTS (SELECT 1 FROM espaco WHERE nome = 'Churrasqueira');
