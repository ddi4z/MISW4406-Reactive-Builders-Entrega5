from pydispatch import dispatcher

from .handlers import HandlerReservaIntegracion

from alpespartners.modulos.comision_recompensa.dominio.eventos import ComisionCreada, RecompensaCreada

dispatcher.connect(HandlerReservaIntegracion.handle_comision_creada, signal=f'{ComisionCreada.__name__}Integracion')
dispatcher.connect(HandlerReservaIntegracion.handle_recompensa_creada, signal=f'{RecompensaCreada.__name__}Integracion')
