
import logging
from dataclasses import dataclass
from asociaciones_estrategicas.seedwork.aplicacion.comandos import Comando

@dataclass
class RealizarPagoComision(Comando):
    id_asociacion: str | None = None
    monto: float | None = None
    monto_vat: float | None = None

@dataclass
class RevertirPagoComision(Comando):
    id_pago: str | None = None
    id_asociacion: str | None = None

def ejecutar(comando: Comando):
    logging.info(f"[SAGA] Publicando comando pagos: {type(comando).__name__} -> {comando}")
