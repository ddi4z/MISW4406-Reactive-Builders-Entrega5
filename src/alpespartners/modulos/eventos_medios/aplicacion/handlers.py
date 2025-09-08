from alpespartners.seedwork.aplicacion.handlers import Handler
from alpespartners.modulos.eventos_medios.infraestructura.despachadores import Despachador

class HandlerReservaIntegracion(Handler):

    @staticmethod
    def handle_evento_creado(evento):
        despachador = Despachador()
        despachador.publicar_evento(evento, 'eventos-evento')

    @staticmethod
    def handle_publicacion_creada(evento):
        despachador = Despachador()
        despachador.publicar_evento(evento, 'eventos-publicacion')

    @staticmethod
    def handle_medio_marketing_creado(evento):
        despachador = Despachador()
        despachador.publicar_evento(evento, 'eventos-medio-marketing')

    @staticmethod
    def handle_plataforma_creada(evento):
        despachador = Despachador()
        despachador.publicar_evento(evento, 'eventos-plataforma')



    