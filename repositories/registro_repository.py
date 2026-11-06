from entities.registro_desempenho import RegistroDesempenho
from entities.treino import Treino
from repositories.base_repository import BaseRepository


class RegistroRepository(BaseRepository):
    def __init__(self, session):
        super().__init__(session, RegistroDesempenho)

    def get_by_treino(self, treino_id):
        return (
            self.session.query(RegistroDesempenho)
            .filter(RegistroDesempenho.treino_id == treino_id)
            .all()
        )

    def get_by_exercicio(self, exercicio_id):
        return (
            self.session.query(RegistroDesempenho)
            .filter(RegistroDesempenho.exercicio_id == exercicio_id)
            .all()
        )

    def get_by_aluno_e_exercicio(self, aluno_id, exercicio_id=None):
        query = (
            self.session.query(RegistroDesempenho)
            .join(Treino, RegistroDesempenho.treino_id == Treino.id)
            .filter(Treino.aluno_id == aluno_id)
        )
        if exercicio_id is not None:
            query = query.filter(RegistroDesempenho.exercicio_id == exercicio_id)
        return query.order_by(Treino.data_treino, RegistroDesempenho.id).all()
