from asociaciones_estrategicas.seedwork.aplicacion.handlers import Handler
from asociaciones_estrategicas.modulos.asociaciones.infraestructura.despachadores import Despachador
from asociaciones_estrategicas.modulos.asociaciones.dominio.eventos import (
    OnboardingIniciado,
    OnboardingFallido,
    OnboardingCancelado,
)


class HandlerAsociacionIntegracion(Handler):

    @staticmethod
    def handle_onboarding_iniciado(evento: OnboardingIniciado):
        Despachador().publicar_evento(evento, "eventos-asociacion")

    @staticmethod
    def handle_onboarding_fallido(evento: OnboardingFallido):
        Despachador().publicar_evento(evento, "eventos-asociacion")

    @staticmethod
    def handle_onboarding_cancelado(evento: OnboardingCancelado):
        Despachador().publicar_evento(evento, "eventos-asociacion")
