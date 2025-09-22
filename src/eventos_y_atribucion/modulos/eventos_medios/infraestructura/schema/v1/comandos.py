from eventos_y_atribucion.seedwork.infraestructura.schema.v1.comandos import ComandoIntegracion
from pulsar.schema import *
from dataclasses import dataclass, field
from pulsar.schema import AvroSchema


"""
    Comandos de pagos
"""
class ComandoRealizarPagoComisionPayload(ComandoIntegracion):
    moneda = String()
    monto = Float()
    metodo_pago = String()
    estado = String()
    pasarela = String()


class ComandoRealizarPagoComision(ComandoIntegracion):
    data = ComandoRealizarPagoComisionPayload()

"""
    Comandos de creacion eventos
"""
class ComandoCrearEventoTrackingPayload(ComandoIntegracion):
    id_correlacion = String()
    id_publicacion = String()
    tipo_evento = String()


class ComandoCrearEventoTracking(ComandoIntegracion):
    data = ComandoCrearEventoTrackingPayload()    


"""
    Comandos de revertir eventos
"""
class ComandoRevertirEventoTrackingPayload(ComandoIntegracion):
    id_correlacion = String()
    id_evento = String()
    motivo = String()

class ComandoRevertirEventoTracking(ComandoIntegracion):
    data = ComandoRevertirEventoTrackingPayload()