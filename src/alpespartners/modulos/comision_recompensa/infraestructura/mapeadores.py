"""Mapeadores para la capa de infraestructura del dominio de externo

En este archivo usted encontrará los diferentes mapeadores
encargados de la transformación entre formatos de dominio y DTOs
"""

from alpespartners.seedwork.dominio.repositorios import Mapeador
import alpespartners.modulos.comision_recompensa.dominio.objetos_valor as ov
from alpespartners.modulos.comision_recompensa.dominio.entidades import Comision, Recompensa 
from alpespartners.modulos.comision_recompensa.infraestructura.dto import (
    ComisionDTO,
    RecompensaDTO
)


class MapeadorRecompensa(Mapeador):
    def obtener_tipo(self) -> type:
        return Recompensa.__class__

    def entidad_a_dto(self, entidad: Recompensa) -> RecompensaDTO:
        dto = RecompensaDTO(
            id = str(entidad.id),
            fecha_creacion = entidad.fecha_creacion,
            fecha_actualizacion = entidad.fecha_actualizacion,
            descripcion = entidad.descripcion,
            id_evento = entidad.id_evento
        )

        return dto

    def dto_a_entidad(self, dto: RecompensaDTO) -> Recompensa:
        entidad = Recompensa(
            id=dto.id,
            fecha_creacion=dto.fecha_creacion,
            fecha_actualizacion=dto.fecha_actualizacion,
            descripcion = dto.descripcion,
            id_evento=dto.id_evento
        )
        return entidad


class MapeadorComision(Mapeador):
    def obtener_tipo(self) -> type:
        return Comision.__class__

    def entidad_a_dto(self, entidad: Comision) -> ComisionDTO:
        dto = ComisionDTO(
            id = str(entidad.id),
            fecha_creacion = entidad.fecha_creacion,
            fecha_actualizacion = entidad.fecha_actualizacion,
            valor = entidad.monto_comision.valor,
            id_evento = entidad.id_evento
        )

        return dto

    def dto_a_entidad(self, dto: ComisionDTO) -> Comision:
        entidad = Comision(
            id=dto.id,
            fecha_creacion=dto.fecha_creacion,
            fecha_actualizacion=dto.fecha_actualizacion,
            descripcion = dto.descripcion,
            id_evento=dto.id_evento,
            valor = ov.MontoComision(dto.valor),
        )
        return entidad

