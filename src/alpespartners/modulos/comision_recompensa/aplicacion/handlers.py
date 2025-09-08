from alpespartners.seedwork.aplicacion.handlers import Handler
from alpespartners.modulos.comision_recompensa.infraestructura.despachadores import Despachador

class HandlerReservaIntegracion(Handler):

    @staticmethod
    def handle_recompensa_creada(evento):
        despachador = Despachador()
        despachador.publicar_evento(evento, 'eventos-recompensa')

    @staticmethod
    def handle_comision_creada(evento):
        despachador = Despachador()
        despachador.publicar_evento(evento, 'eventos-comision')



    