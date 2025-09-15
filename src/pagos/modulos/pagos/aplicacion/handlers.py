from pagos.seedwork.aplicacion.handlers import Handler
from pagos.modulos.pagos.infraestructura.despachadores import Despachador

class HandlerReservaIntegracion(Handler):

    @staticmethod
    def handle_pago_creado(evento):
        despachador = Despachador()
        despachador.publicar_evento(evento, 'eventos-pago')


    