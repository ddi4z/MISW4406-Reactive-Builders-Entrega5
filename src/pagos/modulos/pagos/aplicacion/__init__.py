from pydispatch import dispatcher

from .handlers import HandlerReservaIntegracion

from pagos.modulos.pagos.dominio.eventos import PagoRealizado

dispatcher.connect(HandlerReservaIntegracion.handle_pago_creado, signal=f'{PagoRealizado.__name__}Integracion')

