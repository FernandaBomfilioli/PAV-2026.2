from flask import request
from flask_restful import Resource

from config.database import SessionLocal
from services.desempenho_service import DesempenhoService
from services.exceptions import ApiError


def _resposta_erro(erro):
    return {"erro": str(erro)}, getattr(erro, "status_code", 400)


class RegistroController(Resource):
    def get(self, registro_id=None):
        session = SessionLocal()
        try:
            service = DesempenhoService(session)
            if registro_id is None:
                treino_id = request.args.get("treino_id", type=int)
                exercicio_id = request.args.get("exercicio_id", type=int)
                registros = service.listar(treino_id=treino_id, exercicio_id=exercicio_id)
                return [r.to_dict() for r in registros], 200
            return service.obter(registro_id).to_dict(), 200
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
            service = DesempenhoService(session)
            return service.criar(dados).to_dict(), 201
        except ApiError as erro:
            return _resposta_erro(erro)
        except Exception as erro:  # noqa: BLE001
            return {"erro": f"Erro interno: {erro}"}, 500
        finally:
            session.close()

    def put(self, registro_id):
        session = SessionLocal()
        try:
            dados = request.get_json(silent=True) or {}
            service = DesempenhoService(session)
            return service.atualizar(registro_id, dados).to_dict(), 200
        except ApiError as erro:
            return _resposta_erro(erro)
        except Exception as erro:  # noqa: BLE001
            return {"erro": f"Erro interno: {erro}"}, 500
        finally:
            session.close()

    def delete(self, registro_id):
        session = SessionLocal()
        try:
            service = DesempenhoService(session)
            service.excluir(registro_id)
            return {"mensagem": "Registro excluído com sucesso."}, 200
        except ApiError as erro:
            return _resposta_erro(erro)
        except Exception as erro:  # noqa: BLE001
            return {"erro": f"Erro interno: {erro}"}, 500
        finally:
            session.close()
