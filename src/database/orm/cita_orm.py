from sqlalchemy import Column, Integer, String, DateTime, Enum, ForeignKey
from sqlalchemy.orm import relationship
from src.database.base import Base
import enum

class EstadoCita(enum.Enum):
    Pendiente = "Pendiente"
    Completada = "Completada"
    Cancelada = "Cancelada"

class CitaORM(Base):
    __tablename__ = "citas"

    id = Column(Integer, primary_key=True)
    fecha = Column(DateTime, nullable=False)
    motivo = Column(String(200), nullable=False)

    mascota_id = Column(Integer, ForeignKey("mascotas.id"))
    empleado_id = Column(Integer, ForeignKey("empleados.id"))

    estado = Column(Enum(EstadoCita), default=EstadoCita.Pendiente)

    # Relaciones
    mascota = relationship("MascotaORM", back_populates="citas")
    empleado = relationship("EmpleadoORM", back_populates="citas")
