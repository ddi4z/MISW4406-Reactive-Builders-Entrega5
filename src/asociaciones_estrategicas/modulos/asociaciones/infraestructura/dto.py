"""DTOs para la capa de infrastructura del dominio de vuelos

En este archivo usted encontrará los DTOs (modelos anémicos) de
la infraestructura del dominio de vuelos

"""

from asociaciones_estrategicas.config.db import db
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy import Column, ForeignKey, Integer, Table

import uuid

Base = db.declarative_base()


class AsociacionEstrategica(db.Model):
    __tablename__ = "asociacion_estrategica"
    __table_args__ = {"schema": "db_asociaciones_estrategicas"}

    id = db.Column(db.String(40), primary_key=True, default=lambda: str(uuid.uuid4()))
    id_marca = db.Column(db.String(40), nullable=False)
    id_socio = db.Column(db.String(40), nullable=False)
    tipo = db.Column(db.String(50), nullable=False)
    descripcion = db.Column(db.String(255))
    fecha_inicio = db.Column(db.DateTime(timezone=True), nullable=False)
    fecha_fin = db.Column(db.DateTime(timezone=True), nullable=False)
    fecha_creacion = db.Column(db.DateTime(timezone=True), nullable=False)
    fecha_actualizacion = db.Column(db.DateTime(timezone=True), nullable=True)


class EventosAsociacion(db.Model):
    __tablename__ = "eventos_asociacion"
    __table_args__ = {"schema": "db_asociaciones_estrategicas"}    

    id = db.Column(db.String(40), primary_key=True, default=lambda: str(uuid.uuid4()))
    id_entidad = db.Column(db.String(40), nullable=False)  # referencia a Asociacion.id
    fecha_evento = db.Column(db.DateTime, nullable=False)
    version = db.Column(db.String(10), nullable=False)
    tipo_evento = db.Column(db.String(100), nullable=False)
    formato_contenido = db.Column(db.String(10), nullable=False)
    nombre_servicio = db.Column(db.String(40), nullable=False)
    contenido = db.Column(db.Text, nullable=False)


class AsociacionesAnalitica(db.Model):
    __tablename__ = "analitica_asociaciones"
    __table_args__ = {"schema": "db_asociaciones_estrategicas"}    
    fecha_creacion = db.Column(db.Date, primary_key=True)
    tipo_asociacion = db.Column(db.String(50), primary_key=True)   # Agrupamiento por tipo de asociacion
    total = db.Column(db.Integer, nullable=False, default=0)