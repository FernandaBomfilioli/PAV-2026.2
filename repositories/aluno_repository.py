from entities.aluno import Aluno
from repositories.base_repository import BaseRepository


class AlunoRepository(BaseRepository):
    def __init__(self, session):
        super().__init__(session, Aluno)

    def get_by_email(self, email):
        return self.session.query(Aluno).filter(Aluno.email == email).first()
