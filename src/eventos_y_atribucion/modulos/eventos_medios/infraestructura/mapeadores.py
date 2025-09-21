"""Mapeadores para la capa de infraestructura del dominio de externo

En este archivo usted encontrará los diferentes mapeadores
encargados de la transformación entre formatos de dominio y DTOs
"""

from eventos_y_atribucion.modulos.comision_recompensa.infraestructura.despachadores import unix_time_millis
from eventos_y_atribucion.modulos.eventos_medios.dominio import entidades
from eventos_y_atribucion.modulos.eventos_medios.dominio.eventos import EventoCancelado, EventoCreado, EventoFallido
from eventos_y_atribucion.modulos.eventos_medios.infraestructura.excepciones import NoExisteImplementacionParaTipoFabricaExcepcion
from eventos_y_atribucion.modulos.eventos_medios.infraestructura.schema.v1.eventos import EventoEvento
from eventos_y_atribucion.seedwork.dominio.repositorios import Mapeador
import eventos_y_atribucion.modulos.eventos_medios.dominio.objetos_valor as ov
from eventos_y_atribucion.modulos.eventos_medios.dominio.entidades import Evento, MedioMarketing, Publicacion 
from eventos_y_atribucion.modulos.eventos_medios.infraestructura.dto import (
    MedioMarketingDTO,
    PublicacionDTO,
    EventoDTO
)


class MapeadorMedioMarketing(Mapeador):
    def obtener_tipo(self) -> type:
        return MedioMarketing.__class__

    def entidad_a_dto(self, entidad: MedioMarketing) -> MedioMarketingDTO:
        dto = MedioMarketingDTO(
            id = str(entidad.id),
            fecha_creacion = entidad.fecha_creacion,
            fecha_actualizacion = entidad.fecha_actualizacion,
            nombre_plataforma = entidad.plataforma.nombre,
            publicaciones = [MapeadorPublicacion().entidad_a_dto(pub) for pub in entidad.publicaciones]
        )

        return dto

    def dto_a_entidad(self, dto: MedioMarketingDTO) -> MedioMarketing:
        entidad = MedioMarketing(
            id=dto.id,
            fecha_creacion=dto.fecha_creacion,
            fecha_actualizacion=dto.fecha_actualizacion,
            plataforma = ov.Plataforma(dto.nombre_plataforma),
            publicaciones=[MapeadorPublicacion().dto_a_entidad(pub_dto) for pub_dto in dto.publicaciones]
        )
        return entidad


class MapeadorPublicacion(Mapeador):
    def obtener_tipo(self) -> type:
        return Publicacion

    def entidad_a_dto(self, entidad: Publicacion) -> PublicacionDTO:
        dto = PublicacionDTO()
        dto.id = str(entidad.id)
        dto.fecha_creacion = entidad.fecha_creacion
        dto.fecha_actualizacion = entidad.fecha_actualizacion
        dto.tipo_publicacion = entidad.tipo_publicacion

        if hasattr(entidad, "id_medio_marketing") and entidad.id_medio_marketing:
            dto.id_medio_marketing = str(entidad.id_medio_marketing)

        return dto

    def dto_a_entidad(self, dto: PublicacionDTO) -> Publicacion:
        entidad = Publicacion(
            id=dto.id,
            fecha_creacion=dto.fecha_creacion,
            fecha_actualizacion=dto.fecha_actualizacion
        )
        entidad.tipo_publicacion.valor = dto.tipo_publicacion
        if dto.id_medio_marketing:
            entidad.id_medio_marketing = dto.id_medio_marketing
        return entidad


class MapeadorEvento(Mapeador):
    def obtener_tipo(self) -> type:
        return Evento.__class__

    def entidad_a_dto(self, entidad: Evento) -> EventoDTO:
        dto = EventoDTO(
            id = str(entidad.id),
            fecha_evento = entidad.fecha_evento,
            tipo_evento = entidad.__class__.__name__,
            id_publicacion = str(entidad.id_publicacion),
        )
        return dto

    def dto_a_entidad(self, dto: EventoDTO) -> Evento:
        clase_evento = getattr(entidades, dto.tipo_evento, Evento)
        entidad = clase_evento(
            id=dto.id,
            fecha_evento=dto.fecha_evento,
            id_publicacion=dto.id_publicacion
        )
        return entidad


class MapeadorEventosEvento(Mapeador):

    versions = ("v1",)
    LATEST_VERSION = versions[0]

    def __init__(self):
        self.router = {
            EventoCreado: self._entidad_a_evento_creado,
            EventoCancelado: self._entidad_a_evento_cancelado,
            EventoFallido: self._entidad_a_evento_fallido,
        }

    def obtener_tipo(self) -> type:
        return EventoEvento.__class__

    def es_version_valida(self, version):
        return version in self.versions

    def _entidad_a_evento_creado(self, entidad: EventoCreado, version=LATEST_VERSION):
        from .schema.v1.eventos import EventoEvento, EventoPayload
        payload = EventoPayload(
            id_correlacion=entidad.id_correlacion,
            id_evento=str(entidad.id_evento),
            id_publicacion=str(entidad.id_publicacion),
            tipo_evento=str(entidad.tipo_evento),
            fecha_actualizacion=int(unix_time_millis(entidad.fecha_actualizacion)),
            fecha_creacion=int(unix_time_millis(entidad.fecha_creacion)),
        )
        evento = EventoEvento(id=str(entidad.id_evento))
        evento.time = int(unix_time_millis(entidad.fecha_creacion))
        evento.specversion = str(version)
        evento.type = "Evento"
        evento.estado = "EventoCreado"
        evento.datacontenttype = "AVRO"
        evento.service_name = "eventos"
        evento.data = payload
        return evento


    def _entidad_a_evento_fallido(self, entidad: EventoFallido, version=LATEST_VERSION):
        from .schema.v1.eventos import EventoEvento, EventoPayload
        payload = EventoPayload(
            id_correlacion=entidad.id_correlacion,
            id_evento=str(entidad.id_evento),
            fecha_actualizacion=int(unix_time_millis(entidad.fecha_actualizacion)),
            fecha_creacion=int(unix_time_millis(entidad.fecha_creacion)),
            motivo=entidad.motivo,
        )
        evento = EventoEvento(id=str(entidad.id_evento))
        evento.time = int(unix_time_millis(entidad.fecha_evento))
        evento.specversion = str(version)
        evento.type = "Evento"
        evento.estado = "EventoFallido"
        evento.datacontenttype = "AVRO"
        evento.service_name = "eventos"
        evento.data = payload
        return evento


    def _entidad_a_evento_cancelado(self, entidad: EventoCancelado, version=LATEST_VERSION):
        from .schema.v1.eventos import EventoEvento, EventoPayload
        payload = EventoPayload(
            id_correlacion=entidad.id_correlacion,
            id_evento=str(entidad.id_evento),
            fecha_actualizacion=int(unix_time_millis(entidad.fecha_actualizacion)),
            fecha_creacion=int(unix_time_millis(entidad.fecha_creacion)),
            fecha_cancelacion=int(unix_time_millis(entidad.fecha_cancelacion)),
        )
        evento = EventoEvento(id=str(entidad.id_evento))
        evento.time = int(unix_time_millis(entidad.fecha_cancelacion))
        evento.specversion = str(version)
        evento.type = "Evento"
        evento.estado = "EventoCancelado"
        evento.datacontenttype = "AVRO"
        evento.service_name = "eventos"
        evento.data = payload
        return evento
  

    def entidad_a_dto(self, entidad: EventoEvento, version=LATEST_VERSION):
        if not entidad:
            raise NoExisteImplementacionParaTipoFabricaExcepcion
        func = self.router.get(entidad.__class__, None)
        if not func:
            raise NoExisteImplementacionParaTipoFabricaExcepcion
        return func(entidad, version=version)

    def dto_a_entidad(self, dto: EventoEvento, version=LATEST_VERSION):
        raise NotImplementedError