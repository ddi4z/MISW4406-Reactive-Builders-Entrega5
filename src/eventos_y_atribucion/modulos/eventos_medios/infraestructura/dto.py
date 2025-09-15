"""DTOs para la capa de infrastructura del dominio de vuelos

En este archivo usted encontrará los DTOs (modelos anémicos) de
la infraestructura del dominio de vuelos

"""

from eventos_y_atribucion.config.db import db
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy import Column, ForeignKey, Integer, Table

import uuid

Base = db.declarative_base()

"""DTOs para la capa de infraestructura del dominio de externo

En este archivo usted encontrará los DTOs (modelos anémicos)
para la persistencia con SQLAlchemy
"""

from eventos_y_atribucion.config.db import db
import uuid
from datetime import datetime


class MedioMarketingDTO(db.Model):
    __tablename__ = "medios_marketing"

    id = db.Column(db.String, primary_key=True, default=lambda: str(uuid.uuid4()))
    fecha_creacion = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    fecha_actualizacion = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)

    nombre_plataforma = db.Column(db.String, nullable=False)

  
    publicaciones = db.relationship("PublicacionDTO", back_populates="medio_marketing")


class PublicacionDTO(db.Model):
    __tablename__ = "publicaciones"

    id = db.Column(db.String, primary_key=True, default=lambda: str(uuid.uuid4()))
    fecha_creacion = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    fecha_actualizacion = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)

    tipo_publicacion = db.Column(db.String, nullable=False)


    id_medio_marketing = db.Column(db.String, db.ForeignKey("medios_marketing.id"))
    medio_marketing = db.relationship("MedioMarketingDTO", back_populates="publicaciones")

    eventos = db.relationship("EventoDTO", back_populates="publicacion")


class EventoDTO(db.Model):
    __tablename__ = "eventos"

    id = db.Column(db.String, primary_key=True, default=lambda: str(uuid.uuid4()))
    fecha_evento = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    tipo_evento = db.Column(db.String, nullable=False)

    id_publicacion = db.Column(db.String, db.ForeignKey("publicaciones.id"))
    publicacion = db.relationship("PublicacionDTO", back_populates="eventos")
    
    recompensa = db.relationship("RecompensaDTO", back_populates="evento", uselist=False)

    comision = db.relationship("ComisionDTO", back_populates="evento", uselist=False)
