from sqlalchemy import Column, Integer, String, Numeric, Text, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from database import Base

class Cliente(Base):
    __tablename__ = "clientes"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(100), nullable=False)
    cpf = Column(String(14), unique=True, nullable=False, index=True)
    telefone = Column(String(20), nullable=False)
    endereco = Column(String(200), nullable=True)
    criado_em = Column(DateTime, default=datetime.utcnow)

    pets = relationship("Pet", back_populates="dono", cascade="all, delete-orphan")


class Pet(Base):
    __tablename__ = "pets"

    id = Column(Integer, primary_key=True, index=True)
    cliente_id = Column(Integer, ForeignKey("clientes.id", ondelete="CASCADE"), nullable=False)
    nome = Column(String(80), nullable=False)
    especie = Column(String(50), nullable=False)
    raca = Column(String(50), nullable=True)
    idade_anos = Column(Integer, nullable=True)
    peso_kg = Column(Numeric(5, 2), nullable=True)
    observacoes = Column(Text, nullable=True)
    criado_em = Column(DateTime, default=datetime.utcnow)

    dono = relationship("Cliente", back_populates="pets")