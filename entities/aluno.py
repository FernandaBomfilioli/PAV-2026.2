from datetime import datetime

from sqlalchemy import (
    Column,
    Integer,
    String,
    Date,
    DateTime,
    Numeric,
    CheckConstraint,
)
from sqlalchemy.orm import relationship

from entities.base import Base


class Aluno(Base):
    __tablename__ = "aluno"
    __table_args__ = (
        CheckConstraint("peso IS NULL OR peso >= 0", name="ck_aluno_peso_nao_negativo"),
        CheckConstraint("altura IS NULL OR altura >= 0", name="ck_aluno_altura_nao_negativa"),
    )

    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String(120), nullable=False)
    email = Column(String(120), nullable=False, unique=True)
    data_nascimento = Column(Date, nullable=True)
    peso = Column(Numeric(5, 2), nullable=True)
    altura = Column(Numeric(4, 2), nullable=True)
    objetivo = Column(String(120), nullable=True)
    criado_em = Column(DateTime, default=datetime.utcnow, nullable=False)
    atualizado_em = Column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False
    )

    # Um aluno possui vários treinos.
    treinos = relationship("Treino", back_populates="aluno", lazy="selectin")

    def to_dict(self):
        return {
            "id": self.id,
            "nome": self.nome,
            "email": self.email,
            "data_nascimento": self.data_nascimento.isoformat() if self.data_nascimento else None,
            "peso": float(self.peso) if self.peso is not None else None,
            "altura": float(self.altura) if self.altura is not None else None,
            "objetivo": self.objetivo,
            "criado_em": self.criado_em.isoformat() if self.criado_em else None,
            "atualizado_em": self.atualizado_em.isoformat() if self.atualizado_em else None,
        }

    def __repr__(self):
        return f"<Aluno id={self.id} nome='{self.nome}'>"