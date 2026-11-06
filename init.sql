-- Script de inicializacao do banco de dados (PostgreSQL)
-- Executado automaticamente pelo container do banco.

CREATE TABLE IF NOT EXISTS aluno (
    id SERIAL PRIMARY KEY,
    nome VARCHAR(120) NOT NULL,
    email VARCHAR(120) NOT NULL UNIQUE,
    data_nascimento DATE,
    peso NUMERIC(5, 2),
    altura NUMERIC(4, 2),
    objetivo VARCHAR(120),
    criado_em TIMESTAMP NOT NULL DEFAULT NOW(),
    atualizado_em TIMESTAMP NOT NULL DEFAULT NOW(),
    CONSTRAINT ck_aluno_peso_nao_negativo CHECK (peso IS NULL OR peso >= 0),
    CONSTRAINT ck_aluno_altura_nao_negativa CHECK (altura IS NULL OR altura >= 0)
);

CREATE TABLE IF NOT EXISTS exercicio (
    id SERIAL PRIMARY KEY,
    nome VARCHAR(120) NOT NULL UNIQUE,
    grupo_muscular VARCHAR(60),
    descricao TEXT,
    criado_em TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS treino (
    id SERIAL PRIMARY KEY,
    aluno_id INTEGER NOT NULL REFERENCES aluno(id) ON DELETE RESTRICT,
    data_treino DATE NOT NULL,
    observacao VARCHAR(255),
    criado_em TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_treino_aluno_id ON treino(aluno_id);

CREATE TABLE IF NOT EXISTS registro_desempenho (
    id SERIAL PRIMARY KEY,
    treino_id INTEGER NOT NULL REFERENCES treino(id) ON DELETE CASCADE,
    exercicio_id INTEGER NOT NULL REFERENCES exercicio(id) ON DELETE RESTRICT,
    carga NUMERIC(8, 2) NOT NULL,
    repeticoes INTEGER NOT NULL,
    criado_em TIMESTAMP NOT NULL DEFAULT NOW(),
    atualizado_em TIMESTAMP NOT NULL DEFAULT NOW(),
    CONSTRAINT ck_registro_carga_nao_negativa CHECK (carga >= 0),
    CONSTRAINT ck_registro_repeticoes_positivas CHECK (repeticoes > 0)
);

CREATE INDEX IF NOT EXISTS idx_registro_treino_id ON registro_desempenho(treino_id);
CREATE INDEX IF NOT EXISTS idx_registro_exercicio_id ON registro_desempenho(exercicio_id);
