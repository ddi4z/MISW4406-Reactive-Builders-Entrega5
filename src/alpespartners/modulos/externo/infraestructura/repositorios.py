""" Repositorios para el manejo de persistencia de objetos de dominio en la capa de infrastructura del dominio de vuelos

En este archivo usted encontrará las diferentes repositorios para
persistir objetos dominio (agregaciones) en la capa de infraestructura del dominio de vuelos

"""

from alpespartners.config.db import db
from alpespartners.modulos.externo.dominio.repositorios import RepositorioEventos, RepositorioMediosMarketing, RepositorioPlataformas, RepositorioPublicaciones
from alpespartners.modulos.externo.dominio.entidades import Evento, MedioMarketing, Plataforma, Publicacion
from uuid import UUID


    
    
class RepositorioEventosPostgres(RepositorioEventos):
    def obtener_por_id(self, id: UUID) -> Evento:
        # TODO
        raise NotImplementedError

    def obtener_todos(self) -> list[Evento]:
        # TODO
        raise NotImplementedError

    def agregar(self, entity: Evento):
        # TODO
        raise NotImplementedError

    def actualizar(self, entity: Evento):
        # TODO
        raise NotImplementedError

    def eliminar(self, entity_id: UUID):
        # TODO
        raise NotImplementedError

class RepositorioMediosMarketingPostgres(RepositorioMediosMarketing):
    def obtener_por_id(self, id: UUID) -> MedioMarketing:
        # TODO
        raise NotImplementedError

    def obtener_todos(self) -> list[MedioMarketing]:
        # TODO
        raise NotImplementedError

    def agregar(self, entity: MedioMarketing):
        # TODO
        raise NotImplementedError

    def actualizar(self, entity: MedioMarketing):
        # TODO
        raise NotImplementedError

    def eliminar(self, entity_id: UUID):
        # TODO
        raise NotImplementedError

class RepositorioPlataformasPostgres(RepositorioPlataformas):
    def obtener_por_id(self, id: UUID) -> Plataforma:
        # TODO
        raise NotImplementedError

    def obtener_todos(self) -> list[Plataforma]:
        # TODO
        raise NotImplementedError

    def agregar(self, entity: Plataforma):
        # TODO
        raise NotImplementedError

    def actualizar(self, entity: Plataforma):
        # TODO
        raise NotImplementedError

    def eliminar(self, entity_id: UUID):
        # TODO
        raise NotImplementedError

class RepositorioPublicacionesPostgres(RepositorioPublicaciones):
    def obtener_por_id(self, id: UUID) -> Publicacion:
        # TODO
        raise NotImplementedError

    def obtener_todos(self) -> list[Publicacion]:
        # TODO
        raise NotImplementedError

    def agregar(self, entity: Publicacion):
        # TODO
        raise NotImplementedError

    def actualizar(self, entity: Publicacion):
        # TODO
        raise NotImplementedError

    def eliminar(self, entity_id: UUID):
        # TODO
        raise NotImplementedError
    
