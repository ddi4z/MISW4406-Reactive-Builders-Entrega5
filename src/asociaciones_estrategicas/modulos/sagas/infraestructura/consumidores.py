# src/asociaciones_estrategicas/modulos/sagas/infraestructura/consumidores.py
import logging
import traceback
import threading
import datetime

import pulsar, _pulsar
from pulsar.schema import AvroSchema

from asociaciones_estrategicas.seedwork.infraestructura import utils

TOPIC_ASOCIACIONES = "eventos-asociaciones"
TOPIC_TRACKING     = "eventos-tracking"
TOPIC_EVENTOS      = "eventos-eventos"
TOPIC_PAGOS        = "eventos-pagos"


# Asociaciones
from asociaciones_estrategicas.modulos.asociaciones.infraestructura.schema.v1.eventos import (
    EventoAsociacion  # Debe exponer: onboarding_iniciado, onboarding_fallido, onboarding_cancelado
)
# Tracking
#from tracking.infraestructura.schema.v1.eventos import (
#    EventoTracking  # Debe exponer: tracking_iniciado, inicio_tracking_fallido, tracking_cancelado
#)
# Eventos & Atribución
from eventos_y_atribucion.modulos.eventos_medios.infraestructura.schema.v1.eventos import  (
    EventoEvento  # Debe exponer: evento_creado, evento_fallido, evento_cancelado
)
# Pagos
from pagos.modulos.pagos.infraestructura.schema.v1.eventos import (
    EventoPago  # Debe exponer: reserva_pagada / pago_realizado, pago_fallido, pago_revertido
)


# Asociaciones
from asociaciones_estrategicas.modulos.asociaciones.dominio.eventos import (
    OnboardingIniciado, OnboardingCancelado, OnboardingFallido
)
# Tracking
from asociaciones_estrategicas.modulos.sagas.dominio.eventos.tracking import (
    TrackingIniciado, TrackingCancelado, InicioTrackingFallido
)
# Eventos & Atribución
from asociaciones_estrategicas.modulos.sagas.dominio.eventos.eventos import (
    EventoCreado, EventoCancelado, EventoFallido
)
# Pagos
from asociaciones_estrategicas.modulos.sagas.dominio.eventos.pagos import (
    PagoRealizado, PagoRevertido, PagoFallido
)

# Coordinador
from asociaciones_estrategicas.modulos.sagas.aplicacion.coordinadores.saga_asociaciones import oir_mensaje


def _millis_to_datetime(ms: int) -> datetime.datetime:
    try:
        return datetime.datetime.fromtimestamp(ms / 1000.0)
    except Exception:
        return datetime.datetime.utcnow()


# ------------------ ASOCIACIONES ------------------
def suscribirse_a_eventos_asociaciones(app=None):
    client = None
    try:
        client = pulsar.Client(f"pulsar://{utils.broker_host()}:6650")
        consumer = client.subscribe(
            TOPIC_ASOCIACIONES,
            consumer_type=_pulsar.ConsumerType.Shared,
            subscription_name="sagas-sub-asociaciones",
            schema=AvroSchema(EventoAsociacion),
        )
        while True:
            msg = consumer.receive()
            evt = msg.value()
            logging.info(f"[SAGAS] EventoOnboarding: {evt}")

            if getattr(evt, "onboarding_iniciado", None):
                d = evt.onboarding_iniciado
                oir_mensaje(OnboardingIniciado(
                    id_correlacion=getattr(d, "id_correlacion", None),
                    fecha_creacion=_millis_to_datetime(getattr(d, "fecha_creacion", 0))
                ))

            if getattr(evt, "onboarding_fallido", None):
                d = evt.onboarding_fallido
                oir_mensaje(OnboardingFallido(
                    id_correlacion=getattr(d, "id_correlacion", None),
                    fecha_actualizacion=_millis_to_datetime(getattr(d, "fecha_actualizacion", 0))
                ))

            if getattr(evt, "onboarding_cancelado", None):
                d = evt.onboarding_cancelado
                oir_mensaje(OnboardingCancelado(
                    id_correlacion=getattr(d, "id_correlacion", None),
                    fecha_actualizacion=_millis_to_datetime(getattr(d, "fecha_actualizacion", 0))
                ))

            consumer.acknowledge(msg)
    except Exception:
        logging.error("[SAGAS] ERROR suscribiéndose a eventos-asociaciones")
        traceback.print_exc()
    finally:
        if client:
            client.close()


# ---------------------- TRACKING -------------------
def suscribirse_a_eventos_tracking(app=None):
    client = None
    try:
        client = pulsar.Client(f"pulsar://{utils.broker_host()}:6650")
        consumer = client.subscribe(
            TOPIC_TRACKING,
            consumer_type=_pulsar.ConsumerType.Shared,
            subscription_name="sagas-sub-tracking",
            schema=AvroSchema(EventoAsociacion), #EventoTracking
        )
        while True:
            msg = consumer.receive()
            evt = msg.value()
            logging.info(f"[SAGAS] EventoTracking: {evt}")

            if getattr(evt, "tracking_iniciado", None):
                d = evt.tracking_iniciado
                oir_mensaje(TrackingIniciado(
                    id_correlacion=getattr(d, "id_correlacion", None),
                    fecha_creacion=_millis_to_datetime(getattr(d, "fecha_creacion", 0))
                ))

            if getattr(evt, "inicio_tracking_fallido", None):
                d = evt.inicio_tracking_fallido
                oir_mensaje(InicioTrackingFallido(
                    id_correlacion=getattr(d, "id_correlacion", None),
                    fecha_actualizacion=_millis_to_datetime(getattr(d, "fecha_actualizacion", 0))
                ))

            if getattr(evt, "tracking_cancelado", None):
                d = evt.tracking_cancelado
                oir_mensaje(TrackingCancelado(
                    id_correlacion=getattr(d, "id_correlacion", None),
                    fecha_actualizacion=_millis_to_datetime(getattr(d, "fecha_actualizacion", 0))
                ))

            consumer.acknowledge(msg)
    except Exception:
        logging.error("[SAGAS] ERROR suscribiéndose a eventos-tracking")
        traceback.print_exc()
    finally:
        if client:
            client.close()


# --------------- EVENTOS & ATRIBUCIÓN ---------------
def suscribirse_a_eventos_eventos(app=None):
    client = None
    try:
        client = pulsar.Client(f"pulsar://{utils.broker_host()}:6650")
        consumer = client.subscribe(
            TOPIC_EVENTOS,
            consumer_type=_pulsar.ConsumerType.Shared,
            subscription_name="sagas-sub-eventos",
            schema=AvroSchema(EventoEvento),
        )
        while True:
            msg = consumer.receive()
            evt = msg.value()
            logging.info(f"[SAGAS] EventoAtribucion: {evt}")

            if getattr(evt, "evento_creado", None):
                d = evt.evento_creado
                oir_mensaje(EventoCreado(
                    id_correlacion=getattr(d, "id_correlacion", None),
                    fecha_creacion=_millis_to_datetime(getattr(d, "fecha_creacion", 0))
                ))

            if getattr(evt, "evento_fallido", None):
                d = evt.evento_fallido
                oir_mensaje(EventoFallido(
                    id_correlacion=getattr(d, "id_correlacion", None),
                    fecha_actualizacion=_millis_to_datetime(getattr(d, "fecha_actualizacion", 0))
                ))

            if getattr(evt, "evento_cancelado", None):
                d = evt.evento_cancelado
                oir_mensaje(EventoCancelado(
                    id_correlacion=getattr(d, "id_correlacion", None),
                    fecha_actualizacion=_millis_to_datetime(getattr(d, "fecha_actualizacion", 0))
                ))

            consumer.acknowledge(msg)
    except Exception:
        logging.error("[SAGAS] ERROR suscribiéndose a eventos-eventos")
        traceback.print_exc()
    finally:
        if client:
            client.close()


# ------------------------ PAGOS ---------------------
def suscribirse_a_eventos_pagos(app=None):
    client = None
    try:
        client = pulsar.Client(f"pulsar://{utils.broker_host()}:6650")
        consumer = client.subscribe(
            TOPIC_PAGOS,
            consumer_type=_pulsar.ConsumerType.Shared,
            subscription_name="sagas-sub-pagos",
            schema=AvroSchema(EventoPago),
        )
        while True:
            msg = consumer.receive()
            evt = msg.value()
            logging.info(f"[SAGAS] EventoPago: {evt}")

            if getattr(evt, "reserva_pagada", None):
                d = evt.reserva_pagada
                oir_mensaje(PagoRealizado(
                    id_correlacion=getattr(d, "id_correlacion", None),
                    monto=getattr(d, "monto", None),
                    monto_vat=getattr(d, "monto_vat", None),
                    fecha_creacion=_millis_to_datetime(getattr(d, "fecha_creacion", 0))
                ))

            if getattr(evt, "pago_fallido", None):
                d = evt.pago_fallido
                oir_mensaje(PagoFallido(
                    id_correlacion=getattr(d, "id_correlacion", None),
                    fecha_actualizacion=_millis_to_datetime(getattr(d, "fecha_actualizacion", 0))
                ))

            if getattr(evt, "pago_revertido", None):
                d = evt.pago_revertido
                oir_mensaje(PagoRevertido(
                    id_correlacion=getattr(d, "id_correlacion", None),
                    fecha_actualizacion=_millis_to_datetime(getattr(d, "fecha_actualizacion", 0))
                ))

            consumer.acknowledge(msg)
    except Exception:
        logging.error("[SAGAS] ERROR suscribiéndose a eventos-pagos")
        traceback.print_exc()
    finally:
        if client:
            client.close()


def inicializar_consumidores(app=None):
    threading.Thread(target=suscribirse_a_eventos_asociaciones, args=(app,), daemon=True).start()
    threading.Thread(target=suscribirse_a_eventos_tracking, args=(app,), daemon=True).start()
    threading.Thread(target=suscribirse_a_eventos_eventos,      args=(app,), daemon=True).start()
    threading.Thread(target=suscribirse_a_eventos_pagos,        args=(app,), daemon=True).start()
