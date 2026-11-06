# API Endpoints — Projeto PAV

Base URL (Docker): `http://localhost:5000`. Envie `Content-Type: application/json` nas requisições POST/PUT.

**Padrões**
- Datas no formato `YYYY-MM-DD`.
- Erros padrão: `{"erro": "mensagem"}` com status 4xx/5xx.
- Todos os `GET` retornam JSON.

---

## 1. Alunos

**Endpoints**
- `GET /alunos` → lista todos.
- `GET /alunos/{id}` → obtém um.
- `POST /alunos` → cria.
- `PUT /alunos/{id}` → atualiza (aceita parcial).
- `DELETE /alunos/{id}` → exclui (bloqueado se houver treinos).

**Payload POST**
```json
{
  "nome": "João Silva",
  "email": "joao@email.com",
  "data_nascimento": "1995-03-10",
  "peso": 75.5,
  "altura": 1.80,
  "objetivo": "Hipertrofia"
}
```
Obrigatórios: `nome`, `email`. Demais opcionais (`data_nascimento`, `peso`, `altura`, `objetivo`).

**Payload PUT (parcial)**
```json
{
  "peso": 76.0,
  "objetivo": "Força"
}
```

**Response (exemplo)**
```json
{
  "id": 1,
  "nome": "João Silva",
  "email": "joao@email.com",
  "data_nascimento": "1995-03-10",
  "peso": 75.5,
  "altura": 1.80,
  "objetivo": "Hipertrofia",
  "criado_em": "2026-10-15T10:30:00",
  "atualizado_em": "2026-10-15T10:30:00"
}
```

---

## 2. Exercícios

**Endpoints**
- `GET /exercicios` → lista todos.
- `GET /exercicios/{id}` → obtém um.
- `POST /exercicios` → cria.
- `PUT /exercicios/{id}` → atualiza (parcial).
- `DELETE /exercicios/{id}` → exclui (bloqueado se houver registros).

**Payload POST**
```json
{
  "nome": "Supino reto",
  "grupo_muscular": "Peito",
  "descricao": "Execução com barra"
}
```
Obrigatório: `nome`. `grupo_muscular` e `descricao` opcionais.

**Payload PUT (parcial)**
```json
{
  "grupo_muscular": "Peitoral",
  "descricao": "Execução com barra e peitoral"
}
```

**Response (exemplo)**
```json
{
  "id": 1,
  "nome": "Supino reto",
  "grupo_muscular": "Peito",
  "descricao": "Execução com barra",
  "criado_em": "2026-10-15T10:30:00"
}
```

---

## 3. Treinos

**Endpoints**
- `GET /treinos` → lista todos (opcional `?aluno_id=1`).
- `GET /treinos/{id}` → obtém (inclui `registros`).
- `POST /treinos` → cria.
- `PUT /treinos/{id}` → atualiza (parcial).
- `DELETE /treinos/{id}` → exclui (cascata para registros).

**Payload POST**
```json
{
  "aluno_id": 1,
  "data_treino": "2026-10-15",
  "observacao": "Treino A"
}
```
Obrigatório: `aluno_id`. `data_treino` (se omitido, hoje) e `observacao` opcionais.

**Filtro de listagem**
`GET /treinos?aluno_id=1`

**Payload PUT (parcial)**
```json
{
  "data_treino": "2026-10-16",
  "observacao": "Treino A - revisado"
}
```

**Response (exemplo)**
```json
{
  "id": 1,
  "aluno_id": 1,
  "data_treino": "2026-10-15",
  "observacao": "Treino A",
  "criado_em": "2026-10-15T10:30:00"
}
```

**Response detalhada do GET /treinos/{id}**
Inclui `"registros": [ { ...registro... } ]`.

---

## 4. Registros de Desempenho

**Endpoints**
- `GET /registros` → lista todos (opcional `?treino_id=1` ou `?exercicio_id=1`).
- `GET /registros/{id}` → obtém um.
- `POST /registros` → cria.
- `PUT /registros/{id}` → atualiza (parcial, valida o enviado).
- `DELETE /registros/{id}` → exclui.

**Payload POST**
```json
{
  "treino_id": 1,
  "exercicio_id": 1,
  "carga": 40.5,
  "repeticoes": 12
}
```
Obrigatórios: `treino_id`, `exercicio_id`, `carga`, `repeticoes`. Regras: carga ≥ 0; repetições > 0.

**Filtros de listagem**
```text
GET /registros?treino_id=1
GET /registros?exercicio_id=1
```

**Payload PUT (parcial)**
```json
{
  "carga": 45.0,
  "repeticoes": 10
}
```

**Response (exemplo)**
```json
{
  "id": 1,
  "treino_id": 1,
  "exercicio_id": 1,
  "exercicio_nome": "Supino reto",
  "carga": 40.5,
  "repeticoes": 12,
  "volume": 486.0,
  "criado_em": "2026-10-15T10:30:00",
  "atualizado_em": "2026-10-15T10:30:00"
}
```

---

## 5. Análises

Todos são `GET` e não aceitam body.

### Volume de um treino
`GET /analise/volume-treino/{treino_id}`

**Response (exemplo)**
```json
{
  "treino_id": 1,
  "aluno_id": 1,
  "data_treino": "2026-10-15",
  "quantidade_registros": 2,
  "volume_total": 972.0,
  "detalhes": [
    {
      "registro_id": 1,
      "exercicio_id": 1,
      "exercicio": "Supino reto",
      "carga": 40.5,
      "repeticoes": 12,
      "volume": 486.0
    }
  ]
}
```

### Comparação entre dois períodos (por aluno + exercício)
`GET /analise/comparacao?aluno_id=1&exercicio_id=1`

Parâmetros opcionais:
- `data_inicio_1`, `data_fim_1`, `data_inicio_2`, `data_fim_2` (`YYYY-MM-DD`)
- Se omitidos, usa janela padrão: último período = últimos 30 dias; período anterior = 30 dias imediatamente antes.

**Response (exemplo)**
```json
{
  "aluno_id": 1,
  "exercicio_id": 1,
  "exercicio": "Supino reto",
  "periodo_1": {
    "data_inicio": "2026-09-15",
    "data_fim": "2026-10-14",
    "quantidade_registros": 2,
    "carga_media": 35.0,
    "carga_maxima": 40.0,
    "volume_total": 840.0,
    "repeticoes_total": 24
  },
  "periodo_2": {
    "data_inicio": "2026-10-15",
    "data_fim": "2026-11-13",
    "quantidade_registros": 3,
    "carga_media": 42.0,
    "carga_maxima": 45.0,
    "volume_total": 1260.0,
    "repeticoes_total": 30
  },
  "tendencia": "evolucao",
  "variacao_volume_percentual": 50.0
}
```
Tendência pode ser: `evolucao`, `reducao`, `estavel`, `sem_dados`.

### Frequência de treinos
`GET /analise/frequencia?aluno_id=1`

Parâmetros opcionais: `data_inicio`, `data_fim` (`YYYY-MM-DD`). Padrão: últimos 30 dias.

**Response (exemplo)**
```json
{
  "aluno_id": 1,
  "data_inicio": "2026-10-15",
  "data_fim": "2026-11-13",
  "quantidade_treinos": 5,
  "datas": [
    "2026-10-15",
    "2026-10-20",
    "2026-10-27"
  ]
}
```

---

## Sugestões para a interface gráfica (UX)

- **Formulários:** Aluno (nome, email obrigatórios), Exercício (nome obrigatório), Treino (aluno obrigatório), Registro (treino, exercício, carga, repetições).
- **Listas:** alunos, exercícios e registros com filtros (treino_id, exercicio_id).
- **Dashboard/Analytics:**
  - Seletor de treino → `GET /analise/volume-treino/{treino_id}` (barras por exercício, volume = carga × reps).
  - Comparação de desempenho por exercício → `GET /analise/comparacao`.
  - Frequência → `GET /analise/frequencia` (heatmap/calendário de datas de treino).
- **Mensagens de erro:** usar `erro` do JSON para exibir ao usuário.
