from datetime import datetime

from sqlalchemy import (
    Column,
    Integer,
    Numeric,
    DateTime,
    ForeignKey,
    CheckConstraint,
)
from sqlalchemy.orm import relationship

from entities.base import Base


class RegistroDesempenho(Base):
    __tablename__ = "registro_desempenho"
    __table_args__ = (
        CheckConstraint("carga >= 0", name="ck_registro_carga_nao_negativa"),
        CheckConstraint("repeticoes > 0", name="ck_registro_repeticoes_positivas"),
    )

    id = Column(Integer, primary_key=True, autoincrement=True)
    treino_id = Column(
        Integer,
        ForeignKey("treino.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    exercicio_id = Column(
        Integer,
        ForeignKey("exercicio.id", ondelete="RESTRICT"),
        nullable=False,
        index=True,
    )
    carga = Column(Numeric(8, 2), nullable=False)
    repeticoes = Column(Integer, nullable=False)
    criado_em = Column(DateTime, default=datetime.utcnow, nullable=False)
    atualizado_em = Column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False
    )

    treino = relationship("Treino", back_populates="registros", lazy="selectin")
    exercicio = relationship("Exercicio", back_populates="registros", lazy="selectin")

    @property
    def volume(self):
        """Volume do registro = carga x repetições (RN07)."""
        return float(self.carga) * int(self.repeticoes)

    def to_dict(self):
        return {
            "id": self.id,
            "treino_id": self.treino_id,
            "exercicio_id": self.exercicio_id,
            "exercicio_nome": self.exercicio.nome if self.exercicio else None,
            "carga": float(self.carga),
            "repeticoes": self.repeticoes,
            "volume": self.volume,
            "criado_em": self.criado_em.isoformat() if self.criado_em else None,
            "atualizado_em": self.atualizado_em.isoformat() if self.atualizado_em else None,
        }

    def __repr__(self):
        return f"<RegistroDesempenho id={self.id} treino={self.treino_id} exercicio={self.exercicio_id}>"