from sqlalchemy.exc import IntegrityError

from entities.exercicio import Exercicio
from repositories.exercicio_repository import ExercicioRepository
from services.exceptions import NotFoundError, ValidationError, BusinessRuleError


class ExercicioService:
    def __init__(self, session):
        self.session = session
        self.repo = ExercicioRepository(session)

    def listar(self):
        return self.repo.get_all()

    def obter(self, exercicio_id):
        exercicio = self.repo.get_by_id(exercicio_id)
        if not exercicio:
            raise NotFoundError("Exercício não encontrado.")
        return exercicio

    def criar(self, dados):
        if not isinstance(dados, dict):
            raise ValidationError("Dados inválidos.")
        nome = (dados.get("nome") or "").strip()
        if not nome:
            raise ValidationError("O campo 'nome' é obrigatório.")
        if self.repo.get_by_nome(nome):
            raise ValidationError("Já existe um exercício com este nome.")

        exercicio = Exercicio(
            nome=nome,
            grupo_muscular=(dados.get("grupo_muscular") or "").strip() or None,
            descricao=(dados.get("descricao") or "").strip() or None,
        )
        try:
            return self.repo.create(exercicio)
        except IntegrityError:
            self.session.rollback()
            raise ValidationError("Não foi possível cadastrar o exercício.")

    def atualizar(self, exercicio_id, dados):
        exercicio = self.obter(exercicio_id)
        if not isinstance(dados, dict):
            raise ValidationError("Dados inválidos.")

        if "nome" in dados and dados.get("nome") is not None:
            nome = str(dados.get("nome")).strip()
            if not nome:
                raise ValidationError("O campo 'nome' não pode ficar vazio.")
            existente = self.repo.get_by_nome(nome)
            if existente and existente.id != exercicio.id:
                raise ValidationError("Já existe um exercício com este nome.")
            exercicio.nome = nome

        if "grupo_muscular" in dados:
            valor = dados.get("grupo_muscular")
            exercicio.grupo_muscular = str(valor).strip() if valor else None

        if "descricao" in dados:
            valor = dados.get("descricao")
            exercicio.descricao = str(valor).strip() if valor else None

        try:
            return self.repo.update(exercicio)
        except IntegrityError:
            self.session.rollback()
            raise ValidationError("Não foi possível atualizar o exercício.")

    def excluir(self, exercicio_id):
        exercicio = self.obter(exercicio_id)
        try:
            self.repo.delete(exercicio)
        except IntegrityError:
            self.session.rollback()
            raise BusinessRuleError(
                "Não é possível excluir exercício com registros de desempenho."
            )
        return True
