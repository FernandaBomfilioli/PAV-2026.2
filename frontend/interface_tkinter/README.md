# Interface gráfica — Sistema de Análise de Desempenho em Academia

Interface simples desenvolvida em Python com Tkinter para consumir a API REST.

## Requisitos

- Python 3.10 ou superior
- API em execução em http://localhost:5000
- Biblioteca requests

## Como executar

1. Inicie a API e o banco usando o docker-compose.yml do projeto principal.
2. Abra o terminal dentro desta pasta.
3. Instale a dependência:

   python -m pip install -r requirements.txt

4. Execute a interface:

   python main.py

## Funcionalidades

- Alunos: cadastrar, consultar, atualizar e excluir.
- Exercícios: cadastrar, consultar, atualizar e excluir.
- Treinos: cadastrar e gerenciar treinos associados a alunos.
- Registros: cadastrar e gerenciar registros de desempenho.
- Análises: consultar volume do treino, comparação de desempenho e frequência.

## Configuração

Se a API estiver em outro endereço, altere a variável API_URL no arquivo config.py.

Os campos e as rotas seguem a documentação API_ENDPOINTS.md do projeto principal.

Para cadastrar treinos e registros, os IDs relacionados precisam existir na API.
