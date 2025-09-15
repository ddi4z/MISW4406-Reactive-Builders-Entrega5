"""
DTOs para la capa de infraestructura del dominio de pagos
"""

import uuid
from datetime import datetime
from sqlalchemy import Column, String, DateTime, Float
from pagos.config.db import Base


class PagoDTO(Base):
    __tablename__ = "pagos"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    id_comision = Column(String, nullable=False, default=lambda: str(uuid.uuid4()))

    fecha_creacion = Column(DateTime, nullable=False, default=datetime.utcnow)
    fecha_actualizacion = Column(DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)

    id_correlacion = Column(String, nullable=False, default="")
    moneda = Column(String, nullable=False, default="")
    monto = Column(Float, nullable=False, default=0.0)
    metodo_pago = Column(String, nullable=False, default="")
    estado = Column(String, nullable=False, default="")
    pasarela = Column(String, nullable=False, default="")
    descripcion = Column(String, nullable=True, default="")
