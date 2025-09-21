
import logging
from dataclasses import dataclass
from asociaciones_estrategicas.seedwork.aplicacion.comandos import Comando

@dataclass
class ComandoIniciarTracking(Comando):
    id_asociacion: str | None = None

@dataclass
class ComandoCancelarTracking(Comando):
    id_asociacion: str | None = None

def ejecutar(comando: Comando):
    logging.info(f"[SAGA] Publicando comando tracking: {type(comando).__name__} -> {comando}")
