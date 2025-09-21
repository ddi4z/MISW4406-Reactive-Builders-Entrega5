from eventos_y_atribucion.modulos.eventos_medios.infraestructura.schema.v1.comandos import (
    ComandoCrearEventoTracking, ComandoCrearEventoTrackingPayload, ComandoRealizarPagoComision, ComandoRealizarPagoComisionPayload, ComandoRevertirEventoTracking, ComandoRevertirEventoTrackingPayload
)
from eventos_y_atribucion.modulos.eventos_medios.infraestructura.despachadores import Despachador
from pulsar.schema import AvroSchema




class ServicioEvento:
    def crear_evento(self, evento_dto, in_id_correlacion: str):
        payload = ComandoCrearEventoTrackingPayload(
            id_correlacion = in_id_correlacion,
            id_publicacion = evento_dto.id_publicacion,
            tipo_evento = evento_dto.tipo_evento
        )

        comando = ComandoCrearEventoTracking(
            type="CrearEventoTracking",
            specversion="v1",
            datacontenttype="AVRO",
            service_name="api-eventos",
            data=payload,
        )

        despachador = Despachador()
        despachador.publicar_comando(
            comando,
            topico="comandos-eventos_y_atribucion.crear_evento",
            schema=AvroSchema(ComandoCrearEventoTracking),
        )

    def revertir_evento(self, id_evento:str, motivo:str,in_id_correlacion: str):
        payload = ComandoRevertirEventoTrackingPayload(
            id_correlacion=in_id_correlacion,
            id_evento=id_evento,
            motivo=motivo
        )

        comando = ComandoRevertirEventoTracking(
            type="RevertirEventoTracking",
            specversion="v1",
            datacontenttype="AVRO",
            service_name="api-eventos",
            data=payload,
        )

        despachador = Despachador()
        despachador.publicar_comando(
            comando,
            topico="comandos-eventos_y_atribucion.revertir_evento",
            schema=AvroSchema(ComandoRevertirEventoTracking),
        )        
        
        
class ServicioPago:
    def realizar_pago_comision(self, pago):
        payload = ComandoRealizarPagoComisionPayload(
            moneda = pago.moneda,
            monto=pago.monto,
            metodo_pago=pago.metodo_pago,
            estado=pago.estado,
            pasarela=pago.pasarela
        )
        comando = ComandoRealizarPagoComision(
            type="RealizarPagoComision",   
            data=payload
        )

        despachador = Despachador()
        despachador.publicar_comando(comando, "comandos-pagos.realizar_pago_comision")
        
