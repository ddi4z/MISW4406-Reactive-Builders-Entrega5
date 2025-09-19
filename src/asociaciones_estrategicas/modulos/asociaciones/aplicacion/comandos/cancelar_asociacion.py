# modulos/asociaciones/aplicacion/comandos/cancelar_asociacion.py
from dataclasses import dataclass
from datetime import datetime
import logging
from asociaciones_estrategicas.seedwork.aplicacion.comandos import Comando
from asociaciones_estrategicas.modulos.asociaciones.aplicacion.comandos.base import CrearAsociacionBaseHandler
from asociaciones_estrategicas.modulos.asociaciones.dominio.eventos import OnboardingCancelado
from asociaciones_estrategicas.modulos.asociaciones.dominio.entidades import AsociacionEstrategica
from asociaciones_estrategicas.seedwork.infraestructura.uow import UnidadTrabajoPuerto
from asociaciones_estrategicas.modulos.asociaciones.infraestructura.repositorios import (
    RepositorioEventosAsociacionEstrategica,
)
from asociaciones_estrategicas.seedwork.aplicacion.comandos import ejecutar_commando as comando


# ==========
# Comando
# ==========
@dataclass
class CancelarAsociacionEstrategica(Comando):
    id_correlacion: str
    id_asociacion: str
    motivo: str = ""          # opcional


# ==========
# Handler
# ==========
class CancelarAsociacionHandler(CrearAsociacionBaseHandler):
    """
    Emite evento de compensación sin tocar estado de dominio.
    Idempotente: aunque la asociación no exista o ya esté cancelada, el evento se emite.
    """

    def handle(self, comando: CancelarAsociacionEstrategica):
        # 1) Crear un "carrier" de eventos y adjuntar el de compensación
        agregada = AsociacionEstrategica()
        agregada.agregar_evento(OnboardingCancelado(
            id_correlacion=comando.id_correlacion,
            id_asociacion=comando.id_asociacion,
            motivo=comando.motivo,
            fecha_cancelacion=datetime.now()
        ))

        # 2) Registrar SOLO eventos en outbox (sin persistir entidad)
        repositorio_eventos = self.fabrica_repositorio.crear_objeto(
            RepositorioEventosAsociacionEstrategica
        )

        UnidadTrabajoPuerto.registrar_batch(
            lambda x: None,            # no persistimos entidad
            agregada,                  # pero pasamos el portador para que la UoW recoja sus eventos
            repositorio_eventos_func=repositorio_eventos.agregar,
        )

        # 3) Commit → persiste en outbox y publica EventoAsociacion(estado="CANCELADO")
        UnidadTrabajoPuerto.commit()
        logging.info(f"[SAGA] OnboardingCancelado emitido (corr={comando.id_correlacion}, id={comando.id_asociacion})")


# ==========
# Registro
# ==========
@comando.register(CancelarAsociacionEstrategica)
def ejecutar_comando_cancelar_asociacion(comando: CancelarAsociacionEstrategica):
    handler = CancelarAsociacionHandler()
    handler.handle(comando)
