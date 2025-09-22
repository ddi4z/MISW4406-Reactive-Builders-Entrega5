"""Mapeadores para la capa de infraestructura del dominio de externo

En este archivo usted encontrará los diferentes mapeadores
encargados de la transformación entre formatos de dominio y DTOs
"""


from dataclasses import field
from datetime import datetime
from pagos.modulos.pagos.infraestructura.excepciones import NoExisteImplementacionParaTipoFabricaExcepcion
from pagos.modulos.pagos.dominio.eventos import PagoFallido, PagoRealizado, PagoRevertido
from pagos.modulos.pagos.infraestructura.schema.v1.eventos import EventoPago
from pagos.modulos.pagos.infraestructura.utils import unix_time_millis
from pagos.seedwork.dominio.repositorios import Mapeador
from pagos.modulos.pagos.dominio.entidades import Pago
from pagos.modulos.pagos.infraestructura.dto import PagoDTO


class MapeadorPago(Mapeador):
    def obtener_tipo(self) -> type:
        return Pago.__class__
    



    def entidad_a_dto(self, entidad: Pago) -> PagoDTO:  
        def limpiar_fecha(valor):
            if not valor or valor == "":
                return datetime.now()
            return valor
              
        dto = PagoDTO(
            id=str(entidad.id),
            id_comision=entidad.id_comision,
            id_correlacion = entidad.id_correlacion,
            fecha_creacion=limpiar_fecha(entidad.fecha_creacion),
            fecha_actualizacion=limpiar_fecha(entidad.fecha_actualizacion),
            monto=entidad.monto,
            moneda=entidad.moneda,
            metodo_pago=entidad.metodo_pago,
            estado=entidad.estado,
            pasarela = entidad.pasarela
        )
        return dto

    def dto_a_entidad(self, dto: PagoDTO) -> Pago:
        def normalizar_fecha(valor):
            if not valor or valor == "":
                return datetime.now()
            if isinstance(valor, str):
                try:
                    return datetime.fromisoformat(valor)
                except Exception:
                    return datetime.now()
            return valor
        entidad = Pago(
            id=dto.id,
            id_comision=dto.id_comision,
            id_correlacion=dto.id_correlacion,
            fecha_creacion=normalizar_fecha(dto.fecha_creacion),
            fecha_actualizacion=normalizar_fecha(dto.fecha_actualizacion),
            monto=dto.monto,
            moneda=dto.moneda,
            estado=dto.estado,
            pasarela=dto.pasarela
        )
        return entidad
    
    
    

class MapeadorEventosPago(Mapeador):

    versions = ("v1",)
    LATEST_VERSION = versions[0]

    def __init__(self):
        self.router = {
            PagoRealizado: self._entidad_a_pago_realizado,
            PagoRevertido: self._entidad_a_pago_revertido,
            PagoFallido: self._entidad_a_pago_fallido,
        }

    def obtener_tipo(self) -> type:
        return EventoPago.__class__

    def es_version_valida(self, version):
        return version in self.versions

    def _entidad_a_pago_realizado(self, entidad: PagoRealizado, version=LATEST_VERSION):
        from .schema.v1.eventos import EventoPago, PagoPayload
        payload = PagoPayload(
            id_pago = str(entidad.id_pago),
            id_comision = str(entidad.id_comision),
            id_correlacion = entidad.id_correlacion,
            fecha_actualizacion=int(unix_time_millis(entidad.fecha_actualizacion or datetime.now())),
            fecha_creacion=int(unix_time_millis(entidad.fecha_creacion or datetime.now())),
            fecha_cancelacion=0,
            moneda = entidad.moneda,
            monto = entidad.monto,
            metodo_pago = entidad.metodo_pago,
            estado = entidad.estado,
            pasarela= entidad.pasarela,
            motivo = '',
        )
        evento = EventoPago(id=str(entidad.id_pago))
        evento.time = int(unix_time_millis(entidad.fecha_creacion or datetime.now()))
        evento.specversion = str(version)
        evento.type = "Evento"
        evento.estado = "EventoCreado"
        evento.datacontenttype = "AVRO"
        evento.service_name = "eventos"
        evento.data = payload
        return evento


    def _entidad_a_pago_fallido(self, entidad: PagoFallido, version=LATEST_VERSION):
        from .schema.v1.eventos import EventoPago, PagoPayload
        payload = PagoPayload(
            id_pago = str(entidad.id_pago),
            id_comision = str(entidad.id_comision),
            id_correlacion = entidad.id_correlacion,
            fecha_actualizacion=int(unix_time_millis(entidad.fecha_actualizacion or datetime.now())),
            fecha_creacion=int(unix_time_millis(entidad.fecha_creacion or datetime.now())),
            fecha_cancelacion=0,
            moneda = entidad.moneda,
            monto = entidad.monto,
            metodo_pago = entidad.metodo_pago,
            estado = entidad.estado,
            pasarela= entidad.pasarela,
            motivo = '',
        )
        evento = EventoPago(id=str(entidad.id_pago))
        evento.time = int(unix_time_millis(entidad.fecha_evento or datetime.now()))
        evento.specversion = str(version)
        evento.type = "Evento"
        evento.estado = "EventoFallido"
        evento.datacontenttype = "AVRO"
        evento.service_name = "eventos"
        evento.data = payload
        return evento


    def _entidad_a_pago_revertido(self, entidad: PagoRevertido, version=LATEST_VERSION):
        from .schema.v1.eventos import EventoPago, PagoPayload

        payload = PagoPayload(
            id_pago = str(entidad.id_pago),
            id_comision = str(entidad.id_comision),
            id_correlacion = entidad.id_correlacion,
             fecha_actualizacion=int(unix_time_millis(entidad.fecha_actualizacion or entidad.fecha_evento)),
            fecha_creacion=int(unix_time_millis(entidad.fecha_creacion or entidad.fecha_evento)),
            fecha_cancelacion=int(unix_time_millis(entidad.fecha_cancelacion or entidad.fecha_evento)),
            moneda = entidad.moneda,
            monto = entidad.monto,
            metodo_pago = entidad.metodo_pago,
            estado = entidad.estado,
            pasarela= entidad.pasarela,
            motivo = entidad.motivo,
        )
        evento = EventoPago(id=str(entidad.id_pago))
        evento.time = int(unix_time_millis(entidad.fecha_cancelacion))
        evento.specversion = str(version)
        evento.type = "Evento"
        evento.estado = "EventoCancelado"
        evento.datacontenttype = "AVRO"
        evento.service_name = "eventos"
        evento.data = payload
        return evento
  

    def entidad_a_dto(self, entidad: EventoPago, version=LATEST_VERSION):
        if not entidad:
            raise NoExisteImplementacionParaTipoFabricaExcepcion
        func = self.router.get(entidad.__class__, None)
        if not func:
            raise NoExisteImplementacionParaTipoFabricaExcepcion
        return func(entidad, version=version)

    def dto_a_entidad(self, dto: EventoPago, version=LATEST_VERSION):
        raise NotImplementedError