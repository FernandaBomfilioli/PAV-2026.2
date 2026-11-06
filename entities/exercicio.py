from datetime import datetime

from sqlalchemy import Column, Integer, String, Text, DateTime
from sqlalchemy.orm import relationship

from entities.base import Base


class Exercicio(Base):
    __tablename__ = "exercicio"

    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String(120), nullable=False, unique=True)
    grupo_muscular = Column(String(60), nullable=True)
    descricao = Column(Text, nullable=True)
    criado_em = Column(DateTime, default=datetime.utcnow, nullable=False)

    # Um exercício pode aparecer em vários registros.
    registros = relationship("RegistroDesempenho", back_populates="exercicio", lazy="selectin")

    def to_dict(self):
        return {
            "id": self.id,
            "nome": self.nome,
            "grupo_muscular": self.grupo_muscular,
            "descricao": self.descricao,
            "criado_em": self.criado_em.isoformat() if self.criado_em else None,
        }

    def __repr__(self):
        return f"<Exercicio id={self.id} nome='{self.nome}'>"