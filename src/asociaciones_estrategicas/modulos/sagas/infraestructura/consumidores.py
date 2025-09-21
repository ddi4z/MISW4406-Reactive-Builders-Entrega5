
import logging, datetime
import pulsar, _pulsar
from pulsar.schema import AvroSchema

from asociaciones_estrategicas.seedwork.infraestructura import utils

# Avro schemas de integración — placeholders: ajusta a tus mensajes reales
# from asociaciones_estrategicas.modulos.asociaciones.infraestructura.schema.v1.eventos import OnboardingIniciadoRecord, OnboardingCanceladoRecord, OnboardingFallidoRecord
# from tracking.eventos import EventoTracking
# from eventos_y_atribucion.eventos import EventoEA
# from pagos.eventos import EventoPago

# Eventos de dominio (que entiende la saga)
from asociaciones_estrategicas.modulos.sagas.dominio.eventos.asociaciones import OnboardingIniciado, OnboardingFallido, OnboardingCancelado
from asociaciones_estrategicas.modulos.sagas.dominio.eventos.tracking import TrackingIniciado, InicioTrackingFallido, TrackingCancelado
from asociaciones_estrategicas.modulos.sagas.dominio.eventos.eventos import EventoCreado, EventoFallido, EventoCancelado
from asociaciones_estrategicas.modulos.sagas.dominio.eventos.pagos import PagoRealizado, PagoRevertido, PagoFallido

from asociaciones_estrategicas.modulos.sagas.aplicacion.coordinadores.saga_asociaciones import oir_mensaje

def _millis_to_datetime(ms: int) -> datetime.datetime:
    return datetime.datetime.fromtimestamp(ms / 1000.0)

# TODO: reemplaza los esquemas Avro y mapeos por los reales de tus microservicios
def suscribirse_a_eventos_asociaciones(app=None):
    logging.info("[SAGAS] Suscriptor asociaciones listo (placeholder)")

def suscribirse_a_eventos_tracking(app=None):
    logging.info("[SAGAS] Suscriptor tracking listo (placeholder)")

def suscribirse_a_eventos_eventos(app=None):
    logging.info("[SAGAS] Suscriptor eventos & atribucion listo (placeholder)")

def suscribirse_a_eventos_pagos(app=None):
    logging.info("[SAGAS] Suscriptor pagos listo (placeholder)")

def iniciar_consumidores(app=None):
    import threading
    threading.Thread(target=suscribirse_a_eventos_asociaciones, args=(app,), daemon=True).start()
    threading.Thread(target=suscribirse_a_eventos_tracking, args=(app,), daemon=True).start()
    threading.Thread(target=suscribirse_a_eventos_eventos, args=(app,), daemon=True).start()
    threading.Thread(target=suscribirse_a_eventos_pagos, args=(app,), daemon=True).start()
