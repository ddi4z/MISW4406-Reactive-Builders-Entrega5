from asociaciones_estrategicas.modulos.asociaciones.dominio.eventos import (
    AsociacionCreada,
    AsociacionFinalizada,
)
from asociaciones_estrategicas.seedwork.aplicacion.handlers import Handler
from asociaciones_estrategicas.modulos.asociaciones.infraestructura.despachadores import Despachador


class HandlerAsociacionIntegracion(Handler):

    @staticmethod
    def handle_asociacion_creada(evento: AsociacionCreada):
        despachador = Despachador()
        despachador.publicar_evento(evento, "eventos-asociacion")


    @staticmethod
    def handle_asociacion_finalizada(evento: AsociacionFinalizada):
        despachador = Despachador()
        despachador.publicar_evento(evento, "eventos-asociacion")
