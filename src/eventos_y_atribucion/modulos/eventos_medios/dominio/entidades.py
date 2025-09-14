"""Entidades del dominio de externo

En este archivo usted encontrará las entidades del dominio de externo

"""

from __future__ import annotations
from abc import ABC
from dataclasses import dataclass, field
from datetime import datetime
import uuid



import eventos_y_atribucion.modulos.eventos_medios.dominio.objetos_valor as ov
from eventos_y_atribucion.modulos.eventos_medios.dominio.eventos import EventoCreado, MedioMarketingCreado, PlataformaCreada, PublicacionCreada
from eventos_y_atribucion.seedwork.dominio.entidades import AgregacionRaiz, Entidad

"""
    PUBLICACIONES   
"""

@dataclass
class Publicacion(Entidad):
    tipo_publicacion: ov.TipoPublicacion = field(default_factory=ov.TipoPublicacion)
    id_medio_marketing: int = field(hash=True, default=None)

    

@dataclass
class MedioMarketing(AgregacionRaiz):
    plataforma: ov.Plataforma = field(default_factory=ov.Plataforma)
    publicaciones: list[Publicacion] = field(default_factory=list)

    def crear_medio_marketing(self, medio: MedioMarketing):
        self.plataforma = medio.plataforma
        self.agregar_evento(MedioMarketingCreado(id_medioMarketing=self.id, fecha_creacion=self.fecha_creacion, nombre_plataforma=self.plataforma.nombre))
        
    def crear_publicacion(self, publicacion: Publicacion):
        self.publicaciones.append(publicacion)
        self.agregar_evento(
            PublicacionCreada(
                id_publicacion=publicacion.id,
                id_medioMarketing=self.id,
                fecha_creacion=self.fecha_creacion,
            )
        )


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



