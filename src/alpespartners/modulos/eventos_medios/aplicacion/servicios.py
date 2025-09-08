from alpespartners.modulos.eventos_medios.dominio.repositorios import RepositorioEventos, RepositorioMediosMarketing, RepositorioPublicaciones
from alpespartners.seedwork.aplicacion.servicios import Servicio
from alpespartners.modulos.eventos_medios.dominio.entidades import Evento, MedioMarketing, Publicacion
from alpespartners.modulos.eventos_medios.dominio.fabricas import FabricaEventos, FabricaMediosMarketing, FabricaPublicaciones
from alpespartners.modulos.eventos_medios.infraestructura.fabricas import FabricaRepositorio
from alpespartners.modulos.eventos_medios.infraestructura.repositorios import RepositorioReservas
from alpespartners.seedwork.infraestructura.uow import UnidadTrabajoPuerto
from .mapeadores import MapeadorEvento, MapeadorMedioMarketing, MapeadorPublicacion

from .dto import EventoDTO, MedioMarketingDTO, PublicacionDTO

import asyncio


class ServicioEvento(Servicio):

    def __init__(self):
        self._fabrica_repositorio: FabricaRepositorio = FabricaRepositorio()
        self._fabrica_eventos: FabricaEventos = FabricaEventos()

    @property
    def fabrica_repositorio(self):
        return self._fabrica_repositorio
    
    @property
    def fabrica_eventos(self):
        return self._fabrica_eventos

    def crear_evento(self, evento_dto: EventoDTO) -> EventoDTO:
        evento: Evento = self.fabrica_eventos.crear_objeto(evento_dto, MapeadorEvento())
        evento.crear_evento(evento)

        repositorio = self.fabrica_repositorio.crear_objeto(RepositorioEventos.__class__)

        UnidadTrabajoPuerto.registrar_batch(repositorio.agregar, evento)
        UnidadTrabajoPuerto.savepoint()
        UnidadTrabajoPuerto.commit()

        return self.fabrica_eventos.crear_objeto(evento, MapeadorEvento())

    def obtener_evento_por_id(self, id) -> EventoDTO:
        repositorio = self.fabrica_repositorio.crear_objeto(RepositorioEventos.__class__)
        return self.fabrica_eventos.crear_objeto(repositorio.obtener_por_id(id), MapeadorEvento())
    
class ServicioMedioMarketing(Servicio):
    def __init__(self):
        self._fabrica_repositorio: FabricaRepositorio = FabricaRepositorio()
        self._fabrica_medios_marketing: FabricaMediosMarketing = FabricaMediosMarketing()

    @property
    def fabrica_repositorio(self):
        return self._fabrica_repositorio
    
    @property
    def fabrica_medios_marketing(self):
        return self._fabrica_medios_marketing

    def crear_medio_marketing(self, medio_dto: MedioMarketingDTO) -> MedioMarketingDTO:
        medio: MedioMarketing = self.fabrica_medios_marketing.crear_objeto(medio_dto, MapeadorMedioMarketing())
        medio.crear_medio(medio)

        repositorio = self.fabrica_repositorio.crear_objeto(RepositorioMediosMarketing.__class__)

        UnidadTrabajoPuerto.registrar_batch(repositorio.agregar, medio)
        UnidadTrabajoPuerto.savepoint()
        UnidadTrabajoPuerto.commit()

        return self.fabrica_medios_marketing.crear_objeto(medio, MapeadorMedioMarketing())
    
class ServicioPublicacion(Servicio):

    def __init__(self):
        self._fabrica_repositorio: FabricaRepositorio = FabricaRepositorio()
        self._fabrica_publicaciones: FabricaPublicaciones = FabricaPublicaciones()

    @property
    def fabrica_repositorio(self):
        return self._fabrica_repositorio
    
    @property
    def fabrica_publicaciones(self):
        return self._fabrica_publicaciones

    def crear_publicacion(self, publicacion_dto: PublicacionDTO) -> PublicacionDTO:
        publicacion: Publicacion = self.fabrica_publicaciones.crear_objeto(publicacion_dto, MapeadorPublicacion())
        publicacion.crear_publicacion(publicacion)

        repositorio = self.fabrica_repositorio.crear_objeto(RepositorioPublicaciones._class_)

        UnidadTrabajoPuerto.registrar_batch(repositorio.agregar, publicacion)
        UnidadTrabajoPuerto.savepoint()
        UnidadTrabajoPuerto.commit()

        return self.fabrica_publicaciones.crear_objeto(publicacion, MapeadorPublicacion())

    def obtener_publicacion_por_id(self, id) -> PublicacionDTO:
        repositorio = self.fabrica_repositorio.crear_objeto(RepositorioPublicaciones._class_)
        return self.fabrica_publicaciones.crear_objeto(repositorio.obtener_por_id(id), MapeadorPublicacion())