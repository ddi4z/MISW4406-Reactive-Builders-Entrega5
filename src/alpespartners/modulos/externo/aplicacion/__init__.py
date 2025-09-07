from pydispatch import dispatcher

from .handlers import HandlerReservaIntegracion

from alpespartners.modulos.externo.dominio.eventos import EventoCreado, PublicacionCreada, MedioMarketingCreado, PlataformaCreada

dispatcher.connect(HandlerReservaIntegracion.handle_evento_creado, signal=f'{EventoCreado.__name__}Integracion')
dispatcher.connect(HandlerReservaIntegracion.handle_publicacion_creada, signal=f'{PublicacionCreada.__name__}Integracion')
dispatcher.connect(HandlerReservaIntegracion.handle_medio_marketing_creado, signal=f'{MedioMarketingCreado.__name__}Integracion')
dispatcher.connect(HandlerReservaIntegracion.handle_plataforma_creada, signal=f'{PlataformaCreada.__name__}Integracion')