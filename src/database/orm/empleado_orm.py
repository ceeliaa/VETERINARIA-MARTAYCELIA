from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from src.database.base import Base

class EmpleadoORM(Base):
    __tablename__ = "empleados"

    id = Column(Integer, primary_key=True)
    nombre = Column(String(50), nullable=False)
    apellidos = Column(String(100), nullable=False)
    puesto = Column(String(50), nullable=False)
    telefono = Column(String(20), nullable=False)

    # Relación con citas
    citas = relationship("CitaORM", back_populates="empleado")
