from pydispatch import dispatcher

from .handlers import HandlerReservaIntegracion

from pagos.modulos.pagos.dominio.eventos import PagoCreado

dispatcher.connect(HandlerReservaIntegracion.handle_pago_creado, signal=f'{PagoCreado.__name__}Integracion')

