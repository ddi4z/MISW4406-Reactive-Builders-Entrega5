"""DTOs para la capa de infrastructura del dominio de pagos

En este archivo usted encontrará los DTOs (modelos anémicos) de
la infraestructura del dominio de pagos

"""

from pagos.config.db import db
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy import Column, ForeignKey, Integer, Table

import uuid

Base = db.declarative_base()

"""DTOs para la capa de infraestructura del dominio de externo

En este archivo usted encontrará los DTOs (modelos anémicos)
para la persistencia con SQLAlchemy
"""

from pagos.config.db import db
import uuid
from datetime import datetime


class PagoDTO(db.Model):
    __tablename__ = "pagos"
    __table_args__ = {"schema": "db_pagos"}

    id = Column(db.String, primary_key=True, default=lambda: str(uuid.uuid4()))
    id_comision = Column(db.String, nullable=False, default=lambda: str(uuid.uuid4()))

    fecha_creacion = Column(db.DateTime, nullable=False, default=datetime.utcnow)
    fecha_actualizacion = Column(
        db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow
    )

    id_correlacion = Column(db.String, nullable=False, default="")
    moneda = Column(db.String, nullable=False, default="")
    monto = Column(db.Float, nullable=False, default=0.0)
    metodo_pago = Column(db.String, nullable=False, default="")
    estado = Column(db.String, nullable=False, default="")
    pasarela = Column(db.String, nullable=False, default="")


class EventosPagoDTO(db.Model):
    __tablename__ = "eventos_pago"
    __table_args__ = {"schema": "db_pagos"}

    id = db.Column(db.String(40), primary_key=True, default=lambda: str(uuid.uuid4()))
    id_entidad = db.Column(db.String(40), nullable=False)  # referencia a Pago.id
    fecha_evento = db.Column(db.DateTime, nullable=False)
    version = db.Column(db.String(10), nullable=False)
    tipo_evento = db.Column(db.String(100), nullable=False)
    formato_contenido = db.Column(db.String(10), nullable=False)
    nombre_servicio = db.Column(db.String(40), nullable=False)
    contenido = db.Column(db.Text, nullable=False)