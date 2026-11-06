from controllers.aluno_controller import AlunoController
from controllers.exercicio_controller import ExercicioController
from controllers.treino_controller import TreinoController
from controllers.registro_controller import RegistroController
from controllers.analise_controller import (
    VolumeTreinoController,
    ComparacaoController,
    FrequenciaController,
)


def register_routes(api):
    api.add_resource(AlunoController, "/alunos", "/alunos/<int:aluno_id>")
    api.add_resource(ExercicioController, "/exercicios", "/exercicios/<int:exercicio_id>")
    api.add_resource(TreinoController, "/treinos", "/treinos/<int:treino_id>")
    api.add_resource(RegistroController, "/registros", "/registros/<int:registro_id>")
    api.add_resource(VolumeTreinoController, "/analise/volume-treino/<int:treino_id>")
    api.add_resource(ComparacaoController, "/analise/comparacao")
    api.add_resource(FrequenciaController, "/analise/frequencia")
