from pulsar.schema import *
from pagos.seedwork.infraestructura.schema.v1.eventos import EventoIntegracion
from pagos.seedwork.infraestructura.utils import time_millis
import uuid


# ========== Payload único (campos opcionales) ==========
class PagoPayload(Record):
    id_correlacion = String()
    id_comision = String()

    # datos para "EventoCreado"
    moneda = String(default='')
    monto =  Float(default=0)
    metodo_pago = String(default='')
    estado = String(default='')
    pasarela = String(default='')
    
    motivo = String(default=None)

    fecha_cancelacion = Long(default=0)


# ========== Evento unificado ==========
class EventoPago(EventoIntegracion):
    id = String(default=str(uuid.uuid4()))
    time = Long()
    ingestion = Long(default=time_millis())
    specversion = String()
    type = String() 
    estado = String()
    datacontenttype = String()
    service_name = String()
    data = PagoPayload()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
