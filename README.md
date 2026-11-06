# Sistema de Análise de Desempenho em Academia (API)

API REST em Python/Flask-RESTful com SQLAlchemy e PostgreSQL.

## Execução local
1. Crie o banco `pav` (e `pav_test` para testes) no PostgreSQL.
2. Copie `.env.example` para `.env` e ajuste `DATABASE_URL`.
3. Instale as dependências: `pip install -r requirements.txt`.
4. Rode a API: `python app.py` (porta 5000).

## Execução com Docker
```bash
docker compose up --build
```

## Principais endpoints
- `GET/POST /alunos`, `GET/PUT/DELETE /alunos/<id>`
- `GET/POST /exercicios`, `GET/PUT/DELETE /exercicios/<id>`
- `GET/POST /treinos`, `GET/PUT/DELETE /treinos/<id>` (filtro `?aluno_id=`)
- `GET/POST /registros`, `GET/PUT/DELETE /registros/<id>` (filtros `?treino_id=` e `?exercicio_id=`)
- `GET /analise/volume-treino/<treino_id>`
- `GET /analise/comparacao?aluno_id=&exercicio_id=...`
- `GET /analise/frequencia?aluno_id=...`
