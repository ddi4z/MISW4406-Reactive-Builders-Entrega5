"""DTOs para la capa de infrastructura del dominio de vuelos

En este archivo usted encontrará los DTOs (modelos anémicos) de
la infraestructura del dominio de vuelos

"""

from alpespartners.config.db import db
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy import Column, ForeignKey, Integer, Table

import uuid

Base = db.declarative_base()

"""DTOs para la capa de infraestructura del dominio de externo

En este archivo usted encontrará los DTOs (modelos anémicos)
para la persistencia con SQLAlchemy
"""

from alpespartners.config.db import db
import uuid
from datetime import datetime


class RecompensaDTO(db.Model):
    __tablename__ = "recompensas"

    id = db.Column(db.String, primary_key=True, default=lambda: str(uuid.uuid4()))
    fecha_creacion = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    fecha_actualizacion = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)

    descripcion = db.Column(db.String, nullable=False)

    id_evento = db.Column(db.String, db.ForeignKey("eventos.id"), nullable=True)
    evento = db.relationship("EventoDTO", back_populates="recompensa", uselist=False)


class ComisionDTO(db.Model):
    __tablename__ = "comisiones"


    id = db.Column(db.String, primary_key=True, default=lambda: str(uuid.uuid4()))
    fecha_creacion = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    fecha_actualizacion = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)

    valor = db.Column(db.Integer , nullable=False)
    id_evento = db.Column(db.String, db.ForeignKey("eventos.id"), nullable=True)
    evento = db.relationship("EventoDTO", back_populates="comision", uselist=False)
