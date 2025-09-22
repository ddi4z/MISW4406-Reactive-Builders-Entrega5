from pulsar.schema import *
from pagos.seedwork.infraestructura.schema.v1.comandos import (ComandoIntegracion)

class ComandoRealizarPagoComisionPayload(ComandoIntegracion):
    id_correlacion = String()
    id_comision = String()
    moneda = String()
    monto = Float()
    metodo_pago = String()
    estado = String()
    pasarela = String()
    


class ComandoRealizarPagoComision(ComandoIntegracion):
    data = ComandoRealizarPagoComisionPayload()
    
    
class ComandoRevertirPagoComisionPayload(ComandoIntegracion):
    id_correlacion = String()
    id_pago = String()
    motivo = String()


class ComandoRevertirPagoComision(ComandoIntegracion):
    data = ComandoRevertirPagoComisionPayload()