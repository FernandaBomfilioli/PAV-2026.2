from sqlalchemy.exc import IntegrityError

from entities.aluno import Aluno
from repositories.aluno_repository import AlunoRepository
from repositories.treino_repository import TreinoRepository
from services.exceptions import NotFoundError, ValidationError, BusinessRuleError
from services.utils import parse_date, to_float_or_none


class AlunoService:
    def __init__(self, session):
        self.session = session
        self.repo = AlunoRepository(session)
        self.treino_repo = TreinoRepository(session)

    def listar(self):
        return self.repo.get_all()

    def obter(self, aluno_id):
        aluno = self.repo.get_by_id(aluno_id)
        if not aluno:
            raise NotFoundError("Aluno não encontrado.")
        return aluno

    def criar(self, dados):
        if not isinstance(dados, dict):
            raise ValidationError("Dados inválidos.")
        nome = (dados.get("nome") or "").strip()
        email = (dados.get("email") or "").strip().lower()
        if not nome:
            raise ValidationError("O campo 'nome' é obrigatório.")
        if not email or "@" not in email:
            raise ValidationError("O campo 'email' é obrigatório e deve ser válido.")
        if self.repo.get_by_email(email):
            raise ValidationError("Já existe um aluno com este e-mail.")

        data_nascimento = None
        if dados.get("data_nascimento"):
            data_nascimento = parse_date(dados.get("data_nascimento"), "data_nascimento")

        peso = to_float_or_none(dados.get("peso"), "peso")
        if peso is not None and peso < 0:
            raise ValidationError("O campo 'peso' não pode ser negativo.")
        altura = to_float_or_none(dados.get("altura"), "altura")
        if altura is not None and altura < 0:
            raise ValidationError("O campo 'altura' não pode ser negativo.")

        aluno = Aluno(
            nome=nome,
            email=email,
            data_nascimento=data_nascimento,
            peso=peso,
            altura=altura,
            objetivo=(dados.get("objetivo") or "").strip() or None,
        )
        try:
            return self.repo.create(aluno)
        except IntegrityError:
            self.session.rollback()
            raise ValidationError("Não foi possível cadastrar o aluno (dados duplicados).")

    def atualizar(self, aluno_id, dados):
        aluno = self.obter(aluno_id)
        if not isinstance(dados, dict):
            raise ValidationError("Dados inválidos.")

        if "nome" in dados and dados.get("nome") is not None:
            nome = str(dados.get("nome")).strip()
            if not nome:
                raise ValidationError("O campo 'nome' não pode ficar vazio.")
            aluno.nome = nome

        if "email" in dados and dados.get("email") is not None:
            email = str(dados.get("email")).strip().lower()
            if "@" not in email:
                raise ValidationError("O campo 'email' deve ser válido.")
            existente = self.repo.get_by_email(email)
            if existente and existente.id != aluno.id:
                raise ValidationError("Já existe um aluno com este e-mail.")
            aluno.email = email

        if "data_nascimento" in dados:
            if dados.get("data_nascimento"):
                aluno.data_nascimento = parse_date(dados.get("data_nascimento"), "data_nascimento")
            else:
                aluno.data_nascimento = None

        if "peso" in dados:
            peso = to_float_or_none(dados.get("peso"), "peso")
            if peso is not None and peso < 0:
                raise ValidationError("O campo 'peso' não pode ser negativo.")
            aluno.peso = peso

        if "altura" in dados:
            altura = to_float_or_none(dados.get("altura"), "altura")
            if altura is not None and altura < 0:
                raise ValidationError("O campo 'altura' não pode ser negativo.")
            aluno.altura = altura

        if "objetivo" in dados:
            objetivo = dados.get("objetivo")
            aluno.objetivo = str(objetivo).strip() if objetivo else None

        try:
            return self.repo.update(aluno)
        except IntegrityError:
            self.session.rollback()
            raise ValidationError("Não foi possível atualizar o aluno (dados duplicados).")

    def excluir(self, aluno_id):
        aluno = self.obter(aluno_id)
        if self.treino_repo.get_by_aluno(aluno_id):
            raise BusinessRuleError(
                "Não é possível excluir aluno com treinos registrados."
            )
        try:
            self.repo.delete(aluno)
        except IntegrityError:
            self.session.rollback()
            raise BusinessRuleError(
                "Não é possível excluir aluno com treinos registrados."
            )
        return True
