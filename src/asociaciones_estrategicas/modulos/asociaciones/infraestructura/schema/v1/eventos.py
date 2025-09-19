from pulsar.schema import *
from asociaciones_estrategicas.seedwork.infraestructura.schema.v1.eventos import EventoIntegracion
from asociaciones_estrategicas.seedwork.infraestructura.utils import time_millis
import uuid


# ======================
# Payloads
# ======================


class OnboardingIniciadoPayload(Record):
    id_correlacion = String()          # Saga tracking
    id_asociacion = String()
    id_marca = String()
    id_socio = String()
    tipo = String()
    descripcion = String()
    fecha_inicio = Long()
    fecha_fin = Long()
    fecha_creacion = Long()


class OnboardingFallidoPayload(Record):
    id_correlacion = String()
    id_asociacion = String()
    motivo = String()
    fecha_creacion = Long()


class OnboardingCanceladoPayload(Record):
    id_correlacion = String()
    id_asociacion = String()
    fecha_cancelacion = Long()
    fecha_creacion = Long()


# ======================
# Eventos de integración
# ======================

class EventoOnboardingIniciado(EventoIntegracion):
    id = String(default=str(uuid.uuid4()))
    time = Long()
    ingestion = Long(default=time_millis())
    specversion = String()
    type = String()
    datacontenttype = String()
    service_name = String()
    data = OnboardingIniciadoPayload()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class EventoOnboardingFallido(EventoIntegracion):
    id = String(default=str(uuid.uuid4()))
    time = Long()
    ingestion = Long(default=time_millis())
    specversion = String()
    type = String()
    datacontenttype = String()
    service_name = String()
    data = OnboardingFallidoPayload()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class EventoOnboardingCancelado(EventoIntegracion):
    id = String(default=str(uuid.uuid4()))
    time = Long()
    ingestion = Long(default=time_millis())
    specversion = String()
    type = String()
    datacontenttype = String()
    service_name = String()
    data = OnboardingCanceladoPayload()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)