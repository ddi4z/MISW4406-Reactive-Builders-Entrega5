
import uuid
import datetime
import logging
from dataclasses import dataclass

from asociaciones_estrategicas.seedwork.aplicacion.sagas import CoordinadorOrquestacion, Transaccion, Inicio, Fin
from asociaciones_estrategicas.seedwork.dominio.eventos import EventoDominio

# Comandos (publishers / wrappers)
from asociaciones_estrategicas.modulos.asociaciones.aplicacion.comandos.crear_asociacion import CrearAsociacion
from asociaciones_estrategicas.modulos.asociaciones.aplicacion.comandos.cancelar_asociacion import CancelarAsociacionEstrategica
from asociaciones_estrategicas.modulos.sagas.aplicacion.comandos.tracking import ComandoIniciarTracking, ComandoCancelarTracking
from asociaciones_estrategicas.modulos.sagas.aplicacion.comandos.eventos import ComandoCrearEventoTracking, ComandoRevertirEventoTracking
from asociaciones_estrategicas.modulos.sagas.aplicacion.comandos.pagos import RealizarPagoComision, RevertirPagoComision

# Eventos de dominio que la Saga entiende
from asociaciones_estrategicas.modulos.asociaciones.dominio.eventos import OnboardingIniciado, OnboardingFallido, OnboardingCancelado
from asociaciones_estrategicas.modulos.sagas.dominio.eventos.tracking import TrackingIniciado, InicioTrackingFallido, TrackingCancelado
from asociaciones_estrategicas.modulos.sagas.dominio.eventos.eventos import EventoCreado, EventoFallido, EventoCancelado
from asociaciones_estrategicas.modulos.sagas.dominio.eventos.pagos import PagoRealizado, PagoFallido, PagoRevertido

# Persistencia de saga_log (DTO simple)
from asociaciones_estrategicas.modulos.sagas.infraestructura.dto import SagaLog, db

SAGA_LOG_MEM = {}

class CoordinadorAsociaciones(CoordinadorOrquestacion):
    """Orquestador de la Saga de Asociaciones Estratégicas.
    Pasos (según hoja de ruta):

    1) Gestión Asociaciones:    CrearAsociacion -> OnboardingIniciado   (compensación: CancelarAsociacionEstrategica)  error: OnboardingFallido
    2) Tracking:                ComandoIniciarTracking -> TrackingIniciado   (compensación: ComandoCancelarTracking)   error: InicioTrackingFallido
    3) Eventos & Atribución:    ComandoCrearEventoTracking -> EventoCreado   (compensación: ComandoRevertirEventoTracking) error: EventoFallido
    4) Pagos:                   RealizarPagoComision -> PagoRealizado        (compensación: RevertirPagoComision)      error: PagoFallido
    """
    def __init__(self, id_correlacion: uuid.UUID|None=None) -> None:
        self.id_correlacion = id_correlacion or uuid.uuid4()
        self.inicializar_pasos()

    def inicializar_pasos(self):
        self.pasos = [
            Inicio(index=0),
            Transaccion(index=1, comando=CrearAsociacion,           evento=OnboardingIniciado,   error=OnboardingFallido,       compensacion=CancelarAsociacionEstrategica),
            Transaccion(index=2, comando=ComandoIniciarTracking,    evento=TrackingIniciado,     error=InicioTrackingFallido,   compensacion=ComandoCancelarTracking),
            Transaccion(index=3, comando=ComandoCrearEventoTracking,event=EventoCreado,          error=EventoFallido,           compensacion=ComandoRevertirEventoTracking),
            Transaccion(index=4, comando=RealizarPagoComision,      evento=PagoRealizado,        error=PagoFallido,             compensacion=RevertirPagoComision),
            Fin(index=5),
        ]

    # Hooks básicos del coordinador
    def iniciar(self):
        self.persistir_en_saga_log(self.pasos[0])

    def terminar(self):
        self.persistir_en_saga_log(self.pasos[-1])

    def persistir_en_saga_log(self, mensaje: object):
        try:
            idx = getattr(mensaje, "index", None)
            tipo = type(mensaje).__name__
            now_dt = datetime.datetime.utcnow()
            SAGA_LOG_MEM.setdefault(str(self.id_correlacion), []).append({"index": idx, "tipo": tipo, "ts": now_dt.isoformat()})
            try:
                registro = SagaLog(id_correlacion=str(self.id_correlacion), index=idx or -1, tipo=tipo, timestamp=now_dt)
                db.session.add(registro)
                db.session.commit()
            except Exception as e:
                logging.warning(f"[SAGA_LOG] No se pudo persistir en DB: {e}")
        except Exception:
            logging.exception("[SAGA_LOG] Error registrando en memoria/DB")

# Punto de entrada externo (usado por los consumidores)
_coordinadores: dict[str, CoordinadorAsociaciones] = {}

def _obtener_coordinador(evt: EventoDominio) -> CoordinadorAsociaciones:
    corr = getattr(evt, "id_correlacion", None) or uuid.uuid4()
    coord = _coordinadores.get(str(corr))
    if not coord:
        coord = CoordinadorAsociaciones(corr)
        coord.iniciar()
        _coordinadores[str(corr)] = coord
    return coord

def oir_mensaje(evento: EventoDominio):
    """Recibe un evento de dominio (de cualquiera de los 4 microservicios) y
    delega al coordinador correspondiente por id_correlacion.
    """
    coord = _obtener_coordinador(evento)
    coord.procesar_evento(evento)
