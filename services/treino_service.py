from sqlalchemy.exc import IntegrityError

from entities.treino import Treino
from repositories.treino_repository import TreinoRepository
from repositories.aluno_repository import AlunoRepository
from services.exceptions import NotFoundError, ValidationError, BusinessRuleError
from services.utils import parse_date


class TreinoService:
    def __init__(self, session):
        self.session = session
        self.repo = TreinoRepository(session)
        self.aluno_repo = AlunoRepository(session)

    def listar(self, aluno_id=None):
        if aluno_id is not None:
            return self.repo.get_by_aluno(aluno_id)
        return self.repo.get_all()

    def obter(self, treino_id):
        treino = self.repo.get_by_id(treino_id)
        if not treino:
            raise NotFoundError("Treino não encontrado.")
        return treino

    def criar(self, dados):
        if not isinstance(dados, dict):
            raise ValidationError("Dados inválidos.")
        aluno_id = dados.get("aluno_id")
        if aluno_id is None:
            raise ValidationError("O campo 'aluno_id' é obrigatório.")
        try:
            aluno_id = int(aluno_id)
        except (TypeError, ValueError):
            raise ValidationError("O campo 'aluno_id' deve ser inteiro.")
        if not self.aluno_repo.get_by_id(aluno_id):
            raise NotFoundError("Aluno não encontrado para este treino.")

        data_treino = parse_date(dados.get("data_treino"), "data_treino")

        treino = Treino(
            aluno_id=aluno_id,
            data_treino=data_treino,
            observacao=(dados.get("observacao") or "").strip() or None,
        )
        try:
            return self.repo.create(treino)
        except IntegrityError:
            self.session.rollback()
            raise ValidationError("Não foi possível cadastrar o treino.")

    def atualizar(self, treino_id, dados):
        treino = self.obter(treino_id)
        if not isinstance(dados, dict):
            raise ValidationError("Dados inválidos.")

        if "aluno_id" in dados and dados.get("aluno_id") is not None:
            try:
                novo_aluno_id = int(dados.get("aluno_id"))
            except (TypeError, ValueError):
                raise ValidationError("O campo 'aluno_id' deve ser inteiro.")
            if not self.aluno_repo.get_by_id(novo_aluno_id):
                raise NotFoundError("Aluno não encontrado para este treino.")
            treino.aluno_id = novo_aluno_id

        if "data_treino" in dados and dados.get("data_treino") is not None:
            treino.data_treino = parse_date(dados.get("data_treino"), "data_treino")

        if "observacao" in dados:
            valor = dados.get("observacao")
            treino.observacao = str(valor).strip() if valor else None

        try:
            return self.repo.update(treino)
        except IntegrityError:
            self.session.rollback()
            raise ValidationError("Não foi possível atualizar o treino.")

    def excluir(self, treino_id):
        treino = self.obter(treino_id)
        try:
            self.repo.delete(treino)
        except IntegrityError:
            self.session.rollback()
            raise BusinessRuleError("Não foi possível excluir o treino.")
        return True
