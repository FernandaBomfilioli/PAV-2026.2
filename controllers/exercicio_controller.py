from flask import request
from flask_restful import Resource

from config.database import SessionLocal
from services.exercicio_service import ExercicioService
from services.exceptions import ApiError


def _resposta_erro(erro):
    return {"erro": str(erro)}, getattr(erro, "status_code", 400)


class ExercicioController(Resource):
    def get(self, exercicio_id=None):
        session = SessionLocal()
        try:
            service = ExercicioService(session)
            if exercicio_id is None:
                return [e.to_dict() for e in service.listar()], 200
            return service.obter(exercicio_id).to_dict(), 200
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
            service = ExercicioService(session)
            return service.criar(dados).to_dict(), 201
        except ApiError as erro:
            return _resposta_erro(erro)
        except Exception as erro:  # noqa: BLE001
            return {"erro": f"Erro interno: {erro}"}, 500
        finally:
            session.close()

    def put(self, exercicio_id):
        session = SessionLocal()
        try:
            dados = request.get_json(silent=True) or {}
            service = ExercicioService(session)
            return service.atualizar(exercicio_id, dados).to_dict(), 200
        except ApiError as erro:
            return _resposta_erro(erro)
        except Exception as erro:  # noqa: BLE001
            return {"erro": f"Erro interno: {erro}"}, 500
        finally:
            session.close()

    def delete(self, exercicio_id):
        session = SessionLocal()
        try:
            service = ExercicioService(session)
            service.excluir(exercicio_id)
            return {"mensagem": "Exercício excluído com sucesso."}, 200
        except ApiError as erro:
            return _resposta_erro(erro)
        except Exception as erro:  # noqa: BLE001
            return {"erro": f"Erro interno: {erro}"}, 500
        finally:
            session.close()
