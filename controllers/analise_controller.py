from datetime import date, timedelta
from flask import request
from flask_restful import Resource

from config.database import SessionLocal
from services.analise_service import AnaliseService
from services.exceptions import ApiError, NotFoundError, ValidationError
from services.utils import parse_date


def _resposta_erro(erro):
    return {"erro": str(erro)}, getattr(erro, "status_code", 400)


class VolumeTreinoController(Resource):
    def get(self, treino_id):
        session = SessionLocal()
        try:
            service = AnaliseService(session)
            return service.volume_treino(treino_id), 200
        except ApiError as erro:
            return _resposta_erro(erro)
        except Exception as erro:  # noqa: BLE001
            return {"erro": f"Erro interno: {erro}"}, 500
        finally:
            session.close()


class ComparacaoController(Resource):
    def get(self):
        session = SessionLocal()
        try:
            aluno_id = request.args.get("aluno_id", type=int)
            exercicio_id = request.args.get("exercicio_id", type=int)
            if aluno_id is None or exercicio_id is None:
                raise ValidationError("Os parâmetros 'aluno_id' e 'exercicio_id' são obrigatórios.")

            hoje = date.today()
            data_fim_2 = parse_date(request.args.get("data_fim_2"), "data_fim_2") if request.args.get("data_fim_2") else hoje
            data_inicio_2 = parse_date(request.args.get("data_inicio_2"), "data_inicio_2") if request.args.get("data_inicio_2") else (hoje - timedelta(days=29))
            data_fim_1 = parse_date(request.args.get("data_fim_1"), "data_fim_1") if request.args.get("data_fim_1") else (data_inicio_2 - timedelta(days=1))
            data_inicio_1 = parse_date(request.args.get("data_inicio_1"), "data_inicio_1") if request.args.get("data_inicio_1") else (data_fim_1 - timedelta(days=29))

            service = AnaliseService(session)
            return service.comparar_periodos(
                aluno_id, exercicio_id, data_inicio_1, data_fim_1, data_inicio_2, data_fim_2
            ), 200
        except ApiError as erro:
            return _resposta_erro(erro)
        except Exception as erro:  # noqa: BLE001
            return {"erro": f"Erro interno: {erro}"}, 500
        finally:
            session.close()


class FrequenciaController(Resource):
    def get(self):
        session = SessionLocal()
        try:
            aluno_id = request.args.get("aluno_id", type=int)
            if aluno_id is None:
                raise ValidationError("O parâmetro 'aluno_id' é obrigatório.")
            data_inicio = None
            data_fim = None
            if request.args.get("data_inicio"):
                data_inicio = parse_date(request.args.get("data_inicio"), "data_inicio")
            if request.args.get("data_fim"):
                data_fim = parse_date(request.args.get("data_fim"), "data_fim")

            service = AnaliseService(session)
            return service.frequencia_treinos(aluno_id, data_inicio, data_fim), 200
        except ApiError as erro:
            return _resposta_erro(erro)
        except Exception as erro:  # noqa: BLE001
            return {"erro": f"Erro interno: {erro}"}, 500
        finally:
            session.close()
