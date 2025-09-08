"""Entidades del dominio de externo

En este archivo usted encontrará las entidades del dominio de externo

"""

from __future__ import annotations
from abc import ABC
from dataclasses import dataclass, field
from datetime import datetime
import uuid



import alpespartners.modulos.externo.dominio.objetos_valor as ov
from alpespartners.modulos.externo.dominio.eventos import EventoCreado, MedioMarketingCreado, PlataformaCreada, PublicacionCreada
from alpespartners.seedwork.dominio.entidades import AgregacionRaiz, Entidad

"""
    PUBLICACIONES   
"""

@dataclass
class Publicacion(Entidad):
    tipo_publicacion: ov.TipoPublicacion = field(default_factory=ov.TipoPublicacion)
    def crear_publicacion(self, publicacion: Publicacion):
        MedioMarketing.agregar_evento(PublicacionCreada(id_publicacion=publicacion.id, fecha_creacion=self.fecha_creacion, id_medioMarketing=self.id))
    

@dataclass
class MedioMarketing(AgregacionRaiz):
    plataforma: ov.Plataforma = field(default_factory=ov.Plataforma)
    
    def crear_medio_marketing(self, medio: MedioMarketing):
        self.plataforma = medio.plataforma
        self.agregar_evento(MedioMarketingCreado(id_medioMarketing=self.id, fecha_creacion=self.fecha_creacion, nombre_plataforma=self.plataforma.nombre))
        

"""
    EVENTOS
"""
@dataclass
class Evento(AgregacionRaiz, ABC):
    id_publicacion: uuid.UUID = field(hash=True, default=None)
    fecha_evento: datetime = field(default_factory=datetime.now)
    
    def crear_evento(self, evento: Evento):
        self.id_publicacion = evento.id_publicacion
        self.fecha_evento = evento.fecha_evento

        self.agregar_evento(EventoCreado(id_evento=self.id, id_publicacion=self.id_publicacion, tipo_evento=self.__class__.__name__, fecha_creacion=self.fecha_evento))

class Lead(Evento):
    ...
    
    
class InteraccionPublicacion(Evento):
    ...



