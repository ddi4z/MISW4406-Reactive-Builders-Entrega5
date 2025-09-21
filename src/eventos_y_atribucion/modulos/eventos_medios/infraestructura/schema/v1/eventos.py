from pulsar.schema import *
from eventos_y_atribucion.seedwork.infraestructura.schema.v1.eventos import EventoIntegracion
from eventos_y_atribucion.seedwork.infraestructura.utils import time_millis
import uuid


# ========== Payload único (campos opcionales) ==========
class EventoPayload(Record):
    id_correlacion = String()
    id_evento = String()

    # datos para "EventoCreado"
    id_publicacion = String(default=None)
    tipo_evento = String(default=None)
    fecha_creacion = Long(default=0)
    fecha_actualizacion = Long(default=0)

    motivo = String(default=None)

    fecha_cancelacion = Long(default=0)


# ========== Evento unificado ==========
class EventoEvento(EventoIntegracion):
    id = String(default=str(uuid.uuid4()))
    time = Long()
    ingestion = Long(default=time_millis())
    specversion = String()
    type = String() 
    estado = String()
    datacontenttype = String()
    service_name = String()
    data = EventoPayload()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
