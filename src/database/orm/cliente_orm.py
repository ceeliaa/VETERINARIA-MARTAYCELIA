from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from src.database.base import Base

class ClienteORM(Base):
    __tablename__ = "clientes"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(50), nullable=False)
    apellidos = Column(String(100), nullable=False)
    dni = Column(String(20), unique=True, nullable=False)
    telefono = Column(String(20), nullable=False)
    correo = Column(String(100), nullable=False)

    mascotas = relationship(
        "MascotaORM",
        back_populates="cliente",
        cascade="all, delete"
    )
