
import logging
from dataclasses import dataclass
from asociaciones_estrategicas.seedwork.aplicacion.comandos import Comando

@dataclass
class ComandoCrearEventoTracking(Comando):
    id_asociacion: str | None = None
    payload: dict | None = None

@dataclass
class ComandoRevertirEventoTracking(Comando):
    id_evento: str | None = None
    id_asociacion: str | None = None

def ejecutar(comando: Comando):
    logging.info(f"[SAGA] Publicando comando eventos: {type(comando).__name__} -> {comando}")
