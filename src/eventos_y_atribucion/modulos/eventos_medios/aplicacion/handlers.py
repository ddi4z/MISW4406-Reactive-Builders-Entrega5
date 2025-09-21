from eventos_y_atribucion.modulos.eventos_medios.dominio.eventos import EventoCancelado, EventoCreado, EventoFallido
from eventos_y_atribucion.seedwork.aplicacion.handlers import Handler
from eventos_y_atribucion.modulos.eventos_medios.infraestructura.despachadores import Despachador

class HandlerReservaIntegracion(Handler):
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
        
    @staticmethod
    def handle_evento_creado(evento: EventoCreado):
        Despachador().publicar_evento(evento, "eventos-evento")

    @staticmethod
    def handle_evento_fallido(evento: EventoFallido):
        Despachador().publicar_evento(evento, "eventos-evento")

    @staticmethod
    def handle_evento_cancelado(evento: EventoCancelado):
        Despachador().publicar_evento(evento, "eventos-evento")



    