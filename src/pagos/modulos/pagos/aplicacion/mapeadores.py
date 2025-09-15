import uuid
from pagos.modulos.pagos.dominio.entidades import Pago
from pagos.modulos.pagos.infraestructura.dto import PagoDTO
from pagos.seedwork.aplicacion.dto import Mapeador as AppMap
from pagos.seedwork.dominio.repositorios import Mapeador as RepMap



from datetime import datetime

class MapeadorPagoDTOJson(AppMap):    
    def externo_a_dto(self, externo: dict) -> PagoDTO:
        return PagoDTO(
            id=externo.get("id", str(uuid.uuid4())),
            id_comision=externo.get("id_comision", str(uuid.uuid4())),
            fecha_creacion=externo.get("fecha_creacion", datetime.utcnow()),
            fecha_actualizacion=externo.get("fecha_actualizacion", datetime.utcnow()),
            id_correlacion=externo.get("id_correlacion", ""),
            moneda=externo.get("moneda", ""),
            monto=externo.get("monto", 0.0),
            metodo_pago=externo.get("metodo_pago", ""),
            estado=externo.get("estado", ""),
            pasarela=externo.get("pasarela", ""),
            descripcion=externo.get("descripcion", "")
        )

    def dto_a_externo(self, dto: PagoDTO) -> dict:
        return dto.__dict__


class MapeadorPago(RepMap):
    def obtener_tipo(self) -> type:
        return Pago

    def entidad_a_dto(self, entidad: Pago) -> PagoDTO:
        return PagoDTO(
            id=str(entidad.id),
            id_comision=str(entidad.id_comision),
            fecha_creacion=entidad.fecha_creacion,
            fecha_actualizacion=entidad.fecha_actualizacion,
            id_correlacion=entidad.id_correlacion,
            moneda=entidad.moneda,
            monto=entidad.monto,
            metodo_pago=entidad.metodo_pago,
            estado=entidad.estado,
            pasarela=entidad.pasarela,
        )

    def dto_a_entidad(self, dto: PagoDTO) -> Pago:
        return Pago(
            id=dto.id,
            id_comision=dto.id_comision,
            fecha_creacion=dto.fecha_creacion,
            fecha_actualizacion=dto.fecha_actualizacion,
            id_correlacion=dto.id_correlacion,
            moneda=dto.moneda,
            monto=dto.monto,
            metodo_pago=dto.metodo_pago,
            estado=dto.estado,
            pasarela=dto.pasarela,
        )
