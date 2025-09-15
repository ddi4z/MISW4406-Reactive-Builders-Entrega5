"""Mapeadores para la capa de infraestructura del dominio de externo

En este archivo usted encontrará los diferentes mapeadores
encargados de la transformación entre formatos de dominio y DTOs
"""


from pagos.seedwork.dominio.repositorios import Mapeador
from pagos.modulos.pagos.dominio.entidades import Pago
from pagos.modulos.pagos.infraestructura.dto import PagoDTO


class MapeadorPago(Mapeador):
    def obtener_tipo(self) -> type:
        return Pago.__class__

    def entidad_a_dto(self, entidad: Pago) -> PagoDTO:
        dto = PagoDTO(
            id=str(entidad.id),
            fecha_creacion=entidad.fecha_creacion,
            fecha_actualizacion=entidad.fecha_actualizacion,
            monto=entidad.monto,
            moneda=entidad.moneda,
            id_comision=entidad.id_comision,
            estado=entidad.estado
        )
        return dto

    def dto_a_entidad(self, dto: PagoDTO) -> Pago:
        entidad = Pago(
            id=dto.id,
            fecha_creacion=dto.fecha_creacion,
            fecha_actualizacion=dto.fecha_actualizacion,
            monto=dto.monto,
            moneda=dto.moneda,
            id_comision=dto.id_comision,
            estado=dto.estado
        )
        return entidad