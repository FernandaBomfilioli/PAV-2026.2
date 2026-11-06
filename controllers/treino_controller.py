from flask import request
from flask_restful import Resource

from config.database import SessionLocal
from services.treino_service import TreinoService
from services.exceptions import ApiError


def _resposta_erro(erro):
    return {"erro": str(erro)}, getattr(erro, "status_code", 400)


class TreinoController(Resource):
    def get(self, treino_id=None):
        session = SessionLocal()
        try:
            service = TreinoService(session)
            if treino_id is None:
                aluno_id = request.args.get("aluno_id", type=int)
                treinos = service.listar(aluno_id=aluno_id)
                return [t.to_dict() for t in treinos], 200
            return service.obter(treino_id).to_dict(include_registros=True), 200
        except ApiError as erro:
            return _resposta_erro(erro)
        except Exception as erro:  # noqa: BLE001
            return {"erro": f"Erro interno: {erro}"}, 500
        finally:
            session.close()

    def post(self):
        session = SessionLocal()
        try:
            dados = request.get_json(silent=True) or {}
            service = TreinoService(session)
            return service.criar(dados).to_dict(), 201
        except ApiError as erro:
            return _resposta_erro(erro)
        except Exception as erro:  # noqa: BLE001
            return {"erro": f"Erro interno: {erro}"}, 500
        finally:
            session.close()

    def put(self, treino_id):
        session = SessionLocal()
        try:
            dados = request.get_json(silent=True) or {}
            service = TreinoService(session)
            return service.atualizar(treino_id, dados).to_dict(), 200
        except ApiError as erro:
            return _resposta_erro(erro)
        except Exception as erro:  # noqa: BLE001
            return {"erro": f"Erro interno: {erro}"}, 500
        finally:
            session.close()

    def delete(self, treino_id):
        session = SessionLocal()
        try:
            service = TreinoService(session)
            service.excluir(treino_id)
            return {"mensagem": "Treino excluído com sucesso."}, 200
        except ApiError as erro:
            return _resposta_erro(erro)
        except Exception as erro:  # noqa: BLE001
            return {"erro": f"Erro interno: {erro}"}, 500
        finally:
            session.close()
