from entities.exercicio import Exercicio
from repositories.base_repository import BaseRepository


class ExercicioRepository(BaseRepository):
    def __init__(self, session):
        super().__init__(session, Exercicio)

    def get_by_nome(self, nome):
        return self.session.query(Exercicio).filter(Exercicio.nome == nome).first()
