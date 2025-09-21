
import logging, uuid
from dataclasses import dataclass
from asociaciones_estrategicas.seedwork.aplicacion.comandos import Comando

@dataclass
class CrearAsociacion(Comando):
    id_asociacion: uuid.UUID | None = None

@dataclass
class CancelarAsociacionEstrategica(Comando):
    id_asociacion: uuid.UUID | None = None

def ejecutar(comando: Comando):
    # Aquí publicarías a 'comandos-asociaciones' con Pulsar/Avro.
    logging.info(f"[SAGA] Publicando comando asociaciones: {type(comando).__name__} -> {comando}")
