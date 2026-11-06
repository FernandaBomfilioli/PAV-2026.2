from entities.treino import Treino
from repositories.base_repository import BaseRepository


class TreinoRepository(BaseRepository):
    def __init__(self, session):
        super().__init__(session, Treino)

    def get_by_aluno(self, aluno_id):
        return (
            self.session.query(Treino)
            .filter(Treino.aluno_id == aluno_id)
            .order_by(Treino.data_treino.desc(), Treino.id.desc())
            .all()
        )

    def get_by_aluno_e_periodo(self, aluno_id, data_inicio=None, data_fim=None):
        query = self.session.query(Treino).filter(Treino.aluno_id == aluno_id)
        if data_inicio is not None:
            query = query.filter(Treino.data_treino >= data_inicio)
        if data_fim is not None:
            query = query.filter(Treino.data_treino <= data_fim)
        return query.order_by(Treino.data_treino).all()
