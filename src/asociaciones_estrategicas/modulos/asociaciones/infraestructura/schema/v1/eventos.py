from pulsar.schema import *
from asociaciones_estrategicas.seedwork.infraestructura.schema.v1.eventos import EventoIntegracion
from asociaciones_estrategicas.seedwork.infraestructura.utils import time_millis
import uuid


# ========== Payload único (campos opcionales) ==========
class AsociacionPayload(Record):
    id_correlacion = String()
    id_asociacion = String()

    # datos para "INICIADO"
    id_marca = String(default=None)
    id_socio = String(default=None)
    tipo = String(default=None)
    descripcion = String(default=None)
    fecha_inicio = Long(default=0)
    fecha_fin = Long(default=0)
    fecha_creacion = Long(default=0)

    # datos para "FALLIDO"
    motivo = String(default=None)

    # datos para "CANCELADO"
    fecha_cancelacion = Long(default=0)


# ========== Evento unificado ==========
class EventoAsociacion(EventoIntegracion):
    id = String(default=str(uuid.uuid4()))
    time = Long()
    ingestion = Long(default=time_millis())
    specversion = String()
    type = String()        # siempre "Asociacion"
    estado = String()      # "INICIADO" | "FALLIDO" | "CANCELADO"
    datacontenttype = String()
    service_name = String()
    data = AsociacionPayload()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
