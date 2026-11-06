from datetime import datetime

from sqlalchemy import Column, Integer, String, Date, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from entities.base import Base


class Treino(Base):
    __tablename__ = "treino"

    id = Column(Integer, primary_key=True, autoincrement=True)
    aluno_id = Column(
        Integer,
        ForeignKey("aluno.id", ondelete="RESTRICT"),
        nullable=False,
        index=True,
    )
    data_treino = Column(Date, nullable=False)
    observacao = Column(String(255), nullable=True)
    criado_em = Column(DateTime, default=datetime.utcnow, nullable=False)

    # Relacionamentos com carregamento "selectin" para facilitar a serialização.
    aluno = relationship("Aluno", back_populates="treinos", lazy="selectin")
    registros = relationship(
        "RegistroDesempenho",
        back_populates="treino",
        cascade="all, delete-orphan",
        lazy="selectin",
    )

    def to_dict(self, include_registros=False):
        resultado = {
            "id": self.id,
            "aluno_id": self.aluno_id,
            "data_treino": self.data_treino.isoformat() if self.data_treino else None,
            "observacao": self.observacao,
            "criado_em": self.criado_em.isoformat() if self.criado_em else None,
        }
        if include_registros:
            resultado["registros"] = [r.to_dict() for r in (self.registros or [])]
        return resultado

    def __repr__(self):
        return f"<Treino id={self.id} aluno_id={self.aluno_id} data={self.data_treino}>"