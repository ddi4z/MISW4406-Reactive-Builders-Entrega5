from pagos.modulos.pagos.infraestructura.despachadores import Despachador
from pagos.modulos.pagos.infraestructura.schema.v1.comandos import ComandoRealizarPagoComision, ComandoRealizarPagoComisionPayload, ComandoRevertirPagoComision, ComandoRevertirPagoComisionPayload


class ServicioPago:
    def realizar_pago_comision(self, pago, in_id_correlacion):
        payload = ComandoRealizarPagoComisionPayload(
            id_correlacion = in_id_correlacion,
            id_comision = pago.id_comision,
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
        

    def revertir_pago_comision(self, id_pago:str, motivo:str,in_id_correlacion: str):
        payload = ComandoRevertirPagoComisionPayload(
            id_correlacion=in_id_correlacion,
            id_pago=id_pago,
            motivo=motivo
        )

        comando = ComandoRevertirPagoComision(
            type="RevertirPagoComision",
            specversion="v1",
            datacontenttype="AVRO",
            service_name="api-pagos",
            data=payload,
        )

        despachador = Despachador()
        despachador.publicar_comando(
            comando, 
            topico="comandos-pagos.revertir_pago_comision",
        )        
        print("COMANDO PUBLICADO")