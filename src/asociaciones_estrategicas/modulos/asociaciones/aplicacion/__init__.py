from pydispatch import dispatcher

from .handlers import HandlerAsociacionIntegracion

from asociaciones_estrategicas.modulos.asociaciones.dominio.eventos import (    AsociacionCreada   , AsociacionFinalizada)

# Registrar handlers para publicar eventos de integración
dispatcher.connect(
    HandlerAsociacionIntegracion.handle_asociacion_creada,
    signal=f"{AsociacionCreada.__name__}Integracion",
)

# Registrar handler para el evento de asociación finalizada
#dispatcher.connect(
#    HandlerAsociacionIntegracion.handle_asociacion_finalizada,
#    signal=f"{AsociacionFinalizada.__name__}Integracion",
#)