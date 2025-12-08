from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from src.database.base import Base

class MascotaORM(Base):
    __tablename__ = "mascotas"

    id = Column(Integer, primary_key=True)
    nombre = Column(String(50), nullable=False)
    especie = Column(String(50))
    raza = Column(String(50))
    sexo = Column(String(20))
    edad = Column(Integer)
    estado_salud = Column(String(50))

    cliente_id = Column(Integer, ForeignKey("clientes.id", ondelete="CASCADE"))

    # Relaciones
    cliente = relationship("ClienteORM", back_populates="mascotas")

    citas = relationship(
        "CitaORM",
        back_populates="mascota",
        cascade="all, delete"
    )
