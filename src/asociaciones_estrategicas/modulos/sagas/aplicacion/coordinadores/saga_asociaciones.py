
import uuid, datetime, logging
from dataclasses import dataclass

from asociaciones_estrategicas.seedwork.aplicacion.sagas import (
    CoordinadorOrquestacion, Transaccion, Inicio, Fin
)
from asociaciones_estrategicas.seedwork.dominio.eventos import EventoDominio

from asociaciones_estrategicas.modulos.asociaciones.aplicacion.comandos.crear_asociacion import CrearAsociacion
from asociaciones_estrategicas.modulos.asociaciones.aplicacion.comandos.cancelar_asociacion import CancelarAsociacionEstrategica

from asociaciones_estrategicas.modulos.sagas.aplicacion.comandos.tracking import (
    ComandoIniciarTracking, ComandoCancelarTracking
)
from asociaciones_estrategicas.modulos.sagas.aplicacion.comandos.eventos import (
    ComandoCrearEventoTracking, ComandoRevertirEventoTracking
)
from asociaciones_estrategicas.modulos.sagas.aplicacion.comandos.pagos import (
    RealizarPagoComision, RevertirPagoComision
)

from asociaciones_estrategicas.modulos.asociaciones.dominio.eventos import OnboardingIniciado, OnboardingFallido, OnboardingCancelado
from asociaciones_estrategicas.modulos.sagas.dominio.eventos.tracking import TrackingIniciado, InicioTrackingFallido, TrackingCancelado
from asociaciones_estrategicas.modulos.sagas.dominio.eventos.eventos import EventoCreado, EventoFallido, EventoCancelado
from asociaciones_estrategicas.modulos.sagas.dominio.eventos.pagos import PagoRealizado, PagoFallido, PagoRevertido

from asociaciones_estrategicas.modulos.sagas.infraestructura.dto import SagaLog, db

SAGA_LOG_MEM: dict[str, list[dict]] = {}
_logger = logging.getLogger(__name__)


class CoordinadorAsociaciones(CoordinadorOrquestacion):
    """
    Flujo:
    1) CrearAsociacion -> OnboardingIniciado   | err: OnboardingFallido   | comp: CancelarAsociacionEstrategica
    2) IniciarTracking  -> TrackingIniciado    | err: InicioTrackingFallido| comp: ComandoCancelarTracking
    3) CrearEventoTrack -> EventoCreado        | err: EventoFallido        | comp: ComandoRevertirEventoTracking
    4) RealizarPago     -> PagoRealizado       | err: PagoFallido          | comp: RevertirPagoComision
    """

    def __init__(self, id_correlacion: uuid.UUID | None = None) -> None:
        self.id_correlacion = id_correlacion or uuid.uuid4()
        self.inicializar_pasos()

    def inicializar_pasos(self) -> None:
        self.pasos = [
            Inicio(index=0),
            Transaccion(index=1, comando=CrearAsociacion,            evento=OnboardingIniciado, error=OnboardingFallido,        compensacion=CancelarAsociacionEstrategica),
            Transaccion(index=2, comando=ComandoIniciarTracking,     evento=TrackingIniciado,   error=InicioTrackingFallido,    compensacion=ComandoCancelarTracking),
            Transaccion(index=3, comando=ComandoCrearEventoTracking, evento=EventoCreado,       error=EventoFallido,            compensacion=ComandoRevertirEventoTracking),
            Transaccion(index=4, comando=RealizarPagoComision,       evento=PagoRealizado,      error=PagoFallido,              compensacion=RevertirPagoComision),
            Fin(index=5),
        ]

    def construir_comando(self, paso: Transaccion, evento: EventoDominio | None) -> object:
        """
        Dado el paso a ejecutar y el último evento recibido, construye la instancia
        del comando (con el id_correlacion y los datos mínimos).
        """
        data = {
            "id_correlacion": getattr(evento, "id_correlacion", None) or str(self.id_correlacion)
        }

        cls_cmd = paso.comando
        try:
            return cls_cmd(**data) 
        except TypeError:
            return cls_cmd(data)

    def iniciar(self) -> None:
        self._persistir(self.pasos[0])

    def terminar(self) -> None:
        self._persistir(self.pasos[-1])

    def _persistir(self, mensaje: object) -> None:
        try:
            idx = getattr(mensaje, "index", None)
            tipo = type(mensaje).__name__
            now = datetime.datetime.utcnow()
            SAGA_LOG_MEM.setdefault(str(self.id_correlacion), []).append({"index": idx, "tipo": tipo, "ts": now.isoformat()})
            try:
                db.session.add(SagaLog(id_correlacion=str(self.id_correlacion), index=idx or -1, tipo=tipo, timestamp=now))
                db.session.commit()
            except Exception as e:
                _logger.warning("No se pudo persistir SagaLog en DB: %s", e)
        except Exception:
            _logger.exception("Error registrando SagaLog")


# ====== CONSUMIDORES ======
_coordinadores: dict[str, CoordinadorAsociaciones] = {}

def _obtener_coordinador(evt: EventoDominio) -> CoordinadorAsociaciones:
    corr = getattr(evt, "id_correlacion", None) or uuid.uuid4()
    coord = _coordinadores.get(str(corr))
    if not coord:
        coord = CoordinadorAsociaciones(uuid.UUID(str(corr)))
        coord.iniciar()
        _coordinadores[str(corr)] = coord
    return coord

def oir_mensaje(evento: EventoDominio) -> None:
    """
    Llamado por los consumidores de Pulsar.
    """
    coord = _obtener_coordinador(evento)
    coord.procesar_evento(evento)
