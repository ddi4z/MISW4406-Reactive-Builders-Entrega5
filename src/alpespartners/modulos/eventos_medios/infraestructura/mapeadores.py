"""Mapeadores para la capa de infraestructura del dominio de externo

En este archivo usted encontrará los diferentes mapeadores
encargados de la transformación entre formatos de dominio y DTOs
"""

from alpespartners.modulos.eventos_medios.dominio import entidades
from alpespartners.seedwork.dominio.repositorios import Mapeador
import alpespartners.modulos.eventos_medios.dominio.objetos_valor as ov
from alpespartners.modulos.eventos_medios.dominio.entidades import Evento, MedioMarketing, Publicacion 
from alpespartners.modulos.eventos_medios.infraestructura.dto import (
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
