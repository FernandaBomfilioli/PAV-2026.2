from flask import request
from flask_restful import Resource

from config.database import SessionLocal
from services.aluno_service import AlunoService
from services.exceptions import ValidationError, NotFoundError, BusinessRuleError, ApiError


def _resposta_erro(erro):
    status = getattr(erro, "status_code", 400)
    return {"erro": str(erro)}, status


class AlunoController(Resource):
    def get(self, aluno_id=None):
        session = SessionLocal()
        try:
            service = AlunoService(session)
            if aluno_id is None:
                alunos = service.listar()
                return [a.to_dict() for a in alunos], 200
            aluno = service.obter(aluno_id)
            return aluno.to_dict(), 200
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
            service = AlunoService(session)
            aluno = service.criar(dados)
            return aluno.to_dict(), 201
        except ApiError as erro:
            return _resposta_erro(erro)
        except Exception as erro:  # noqa: BLE001
            return {"erro": f"Erro interno: {erro}"}, 500
        finally:
            session.close()

    def put(self, aluno_id):
        session = SessionLocal()
        try:
            dados = request.get_json(silent=True) or {}
            service = AlunoService(session)
            aluno = service.atualizar(aluno_id, dados)
            return aluno.to_dict(), 200
        except ApiError as erro:
            return _resposta_erro(erro)
        except Exception as erro:  # noqa: BLE001
            return {"erro": f"Erro interno: {erro}"}, 500
        finally:
            session.close()

    def delete(self, aluno_id):
        session = SessionLocal()
        try:
            service = AlunoService(session)
            service.excluir(aluno_id)
            return {"mensagem": "Aluno excluído com sucesso."}, 200
        except ApiError as erro:
            return _resposta_erro(erro)
        except Exception as erro:  # noqa: BLE001
            return {"erro": f"Erro interno: {erro}"}, 500
        finally:
            session.close()
