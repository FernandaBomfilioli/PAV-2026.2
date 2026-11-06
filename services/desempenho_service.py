from decimal import Decimal

from sqlalchemy.exc import IntegrityError

from entities.registro_desempenho import RegistroDesempenho
from repositories.registro_repository import RegistroRepository
from repositories.treino_repository import TreinoRepository
from repositories.exercicio_repository import ExercicioRepository
from services.exceptions import NotFoundError, ValidationError, BusinessRuleError
from services.utils import to_float_or_none


class DesempenhoService:
    def __init__(self, session):
        self.session = session
        self.repo = RegistroRepository(session)
        self.treino_repo = TreinoRepository(session)
        self.exercicio_repo = ExercicioRepository(session)

    def listar(self, treino_id=None, exercicio_id=None):
        if treino_id is not None:
            return self.repo.get_by_treino(treino_id)
        if exercicio_id is not None:
            return self.repo.get_by_exercicio(exercicio_id)
        return self.repo.get_all()

    def obter(self, registro_id):
        registro = self.repo.get_by_id(registro_id)
        if not registro:
            raise NotFoundError("Registro de desempenho não encontrado.")
        return registro

    def _validar_dados(self, dados, exigir_todos=True):
        if not isinstance(dados, dict):
            raise ValidationError("Dados inválidos.")

        treino_id = dados.get("treino_id")
        exercicio_id = dados.get("exercicio_id")
        carga = dados.get("carga")
        repeticoes = dados.get("repeticoes")

        if exigir_todos or treino_id is not None:
            if treino_id is None:
                raise ValidationError("O campo 'treino_id' é obrigatório.")
            try:
                treino_id = int(treino_id)
            except (TypeError, ValueError):
                raise ValidationError("O campo 'treino_id' deve ser inteiro.")
            if not self.treino_repo.get_by_id(treino_id):
                raise NotFoundError("Treino não encontrado para este registro.")

        if exigir_todos or exercicio_id is not None:
            if exercicio_id is None:
                raise ValidationError("O campo 'exercicio_id' é obrigatório.")
            try:
                exercicio_id = int(exercicio_id)
            except (TypeError, ValueError):
                raise ValidationError("O campo 'exercicio_id' deve ser inteiro.")
            if not self.exercicio_repo.get_by_id(exercicio_id):
                raise NotFoundError("Exercício não encontrado para este registro.")

        if exigir_todos or carga is not None:
            if carga is None:
                raise ValidationError("O campo 'carga' é obrigatório.")
            carga = to_float_or_none(carga, "carga")
            if carga is None or carga < 0:
                raise ValidationError("A carga não pode ser negativa (RN01).")

        if exigir_todos or repeticoes is not None:
            if repeticoes is None:
                raise ValidationError("O campo 'repeticoes' é obrigatório.")
            try:
                repeticoes = int(repeticoes)
            except (TypeError, ValueError):
                raise ValidationError("O campo 'repeticoes' deve ser inteiro.")
            if repeticoes <= 0:
                raise ValidationError("A quantidade de repetições deve ser maior que zero (RN02).")

        return treino_id, exercicio_id, carga, repeticoes

    def criar(self, dados):
        treino_id, exercicio_id, carga, repeticoes = self._validar_dados(dados, exigir_todos=True)

        # RN06: dados obrigatórios já validados acima.
        registro = RegistroDesempenho(
            treino_id=treino_id,
            exercicio_id=exercicio_id,
            carga=Decimal(str(carga)),
            repeticoes=repeticoes,
        )
        try:
            return self.repo.create(registro)
        except IntegrityError:
            self.session.rollback()
            raise ValidationError("Não foi possível registrar o desempenho.")

    def atualizar(self, registro_id, dados):
        registro = self.obter(registro_id)
        if not isinstance(dados, dict):
            raise ValidationError("Dados inválidos.")

        # Atualização parcial, mas valida o que for enviado.
        if "treino_id" in dados and dados.get("treino_id") is not None:
            try:
                novo_treino_id = int(dados.get("treino_id"))
            except (TypeError, ValueError):
                raise ValidationError("O campo 'treino_id' deve ser inteiro.")
            if not self.treino_repo.get_by_id(novo_treino_id):
                raise NotFoundError("Treino não encontrado para este registro.")
            registro.treino_id = novo_treino_id

        if "exercicio_id" in dados and dados.get("exercicio_id") is not None:
            try:
                novo_exercicio_id = int(dados.get("exercicio_id"))
            except (TypeError, ValueError):
                raise ValidationError("O campo 'exercicio_id' deve ser inteiro.")
            if not self.exercicio_repo.get_by_id(novo_exercicio_id):
                raise NotFoundError("Exercício não encontrado para este registro.")
            registro.exercicio_id = novo_exercicio_id

        if "carga" in dados and dados.get("carga") is not None:
            carga = to_float_or_none(dados.get("carga"), "carga")
            if carga is None or carga < 0:
                raise ValidationError("A carga não pode ser negativa (RN01).")
            registro.carga = Decimal(str(carga))

        if "repeticoes" in dados and dados.get("repeticoes") is not None:
            try:
                repeticoes = int(dados.get("repeticoes"))
            except (TypeError, ValueError):
                raise ValidationError("O campo 'repeticoes' deve ser inteiro.")
            if repeticoes <= 0:
                raise ValidationError("A quantidade de repetições deve ser maior que zero (RN02).")
            registro.repeticoes = repeticoes

        try:
            return self.repo.update(registro)
        except IntegrityError:
            self.session.rollback()
            raise ValidationError("Não foi possível atualizar o registro.")

    def excluir(self, registro_id):
        registro = self.obter(registro_id)
        try:
            self.repo.delete(registro)
        except IntegrityError:
            self.session.rollback()
            raise BusinessRuleError("Não foi possível excluir o registro.")
        return True
