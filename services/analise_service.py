from datetime import date, timedelta

from repositories.registro_repository import RegistroRepository
from repositories.treino_repository import TreinoRepository
from repositories.exercicio_repository import ExercicioRepository
from services.exceptions import NotFoundError


class AnaliseService:
    def __init__(self, session):
        self.session = session
        self.registro_repo = RegistroRepository(session)
        self.treino_repo = TreinoRepository(session)
        self.exercicio_repo = ExercicioRepository(session)

    def volume_treino(self, treino_id):
        treino = self.treino_repo.get_by_id(treino_id)
        if not treino:
            raise NotFoundError("Treino não encontrado.")
        registros = self.registro_repo.get_by_treino(treino_id)

        detalhes = []
        total = 0.0
        for r in registros:
            volume = float(r.carga) * int(r.repeticoes)
            total += volume
            detalhes.append(
                {
                    "registro_id": r.id,
                    "exercicio_id": r.exercicio_id,
                    "exercicio": r.exercicio.nome if r.exercicio else None,
                    "carga": float(r.carga),
                    "repeticoes": r.repeticoes,
                    "volume": volume,
                }
            )

        return {
            "treino_id": treino.id,
            "aluno_id": treino.aluno_id,
            "data_treino": treino.data_treino.isoformat(),
            "quantidade_registros": len(registros),
            "volume_total": total,
            "detalhes": detalhes,
        }

    def frequencia_treinos(self, aluno_id, data_inicio=None, data_fim=None):
        if data_inicio is None:
            data_inicio = date.today() - timedelta(days=30)
        if data_fim is None:
            data_fim = date.today()
        treinos = self.treino_repo.get_by_aluno_e_periodo(aluno_id, data_inicio, data_fim)
        return {
            "aluno_id": aluno_id,
            "data_inicio": data_inicio.isoformat(),
            "data_fim": data_fim.isoformat(),
            "quantidade_treinos": len(treinos),
            "datas": [t.data_treino.isoformat() for t in treinos],
        }

    def _metricas_periodo(self, registros, data_inicio, data_fim):
        filtrados = [
            r
            for r in registros
            if data_inicio <= r.treino.data_treino <= data_fim
        ]
        if not filtrados:
            return {
                "quantidade_registros": 0,
                "carga_media": 0.0,
                "carga_maxima": 0.0,
                "volume_total": 0.0,
                "repeticoes_total": 0,
            }
        cargas = [float(r.carga) for r in filtrados]
        volumes = [float(r.carga) * int(r.repeticoes) for r in filtrados]
        return {
            "quantidade_registros": len(filtrados),
            "carga_media": round(sum(cargas) / len(cargas), 2),
            "carga_maxima": max(cargas),
            "volume_total": round(sum(volumes), 2),
            "repeticoes_total": sum(r.repeticoes for r in filtrados),
        }

    def comparar_periodos(self, aluno_id, exercicio_id, data_inicio_1, data_fim_1, data_inicio_2, data_fim_2):
        exercicio = self.exercicio_repo.get_by_id(exercicio_id)
        if not exercicio:
            raise NotFoundError("Exercício não encontrado.")
        registros = self.registro_repo.get_by_aluno_e_exercicio(aluno_id, exercicio_id)

        periodo_1 = self._metricas_periodo(registros, data_inicio_1, data_fim_1)
        periodo_2 = self._metricas_periodo(registros, data_inicio_2, data_fim_2)

        # Comparação pelo volume total (indicador mais completo).
        v1 = periodo_1["volume_total"]
        v2 = periodo_2["volume_total"]
        if v1 == 0 and v2 == 0:
            tendencia = "sem_dados"
            variacao = 0.0
        elif v1 == 0:
            tendencia = "evolucao"
            variacao = 100.0
        else:
            variacao = round(((v2 - v1) / v1) * 100, 2)
            if variacao > 0:
                tendencia = "evolucao"
            elif variacao < 0:
                tendencia = "reducao"
            else:
                tendencia = "estavel"

        return {
            "aluno_id": aluno_id,
            "exercicio_id": exercicio_id,
            "exercicio": exercicio.nome,
            "periodo_1": {
                "data_inicio": data_inicio_1.isoformat(),
                "data_fim": data_fim_1.isoformat(),
                **periodo_1,
            },
            "periodo_2": {
                "data_inicio": data_inicio_2.isoformat(),
                "data_fim": data_fim_2.isoformat(),
                **periodo_2,
            },
            "tendencia": tendencia,
            "variacao_volume_percentual": variacao,
        }
