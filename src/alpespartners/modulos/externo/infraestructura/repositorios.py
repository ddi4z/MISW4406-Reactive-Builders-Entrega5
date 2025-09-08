from alpespartners.config.db import db
from alpespartners.modulos.externo.dominio.repositorios import (
    RepositorioEventos,
    RepositorioMediosMarketing,
    RepositorioPublicaciones
)
from alpespartners.modulos.externo.dominio.entidades import Evento, MedioMarketing, Publicacion
from .mapeadores import (
    MapeadorMedioMarketing,
    MapeadorPublicacion,
    MapeadorEvento
)
from alpespartners.modulos.externo.dominio.fabricas import (
    FabricaMediosMarketing,
    FabricaEventos,
    FabricaPublicaciones
)
from uuid import UUID


class RepositorioEventosPostgres(RepositorioEventos):
    def __init__(self):
        super().__init__()
        self._fabrica_eventos = FabricaEventos()

    @property
    def fabrica_eventos(self):
        return self._fabrica_eventos

    def obtener_por_id(self, id: UUID) -> Evento:
        dto = db.session.query(self.fabrica_eventos.dto()).filter_by(id=str(id)).first()
        if dto:
            return self.fabrica_eventos.crear_objeto(dto, MapeadorEvento())
        return None

    def obtener_todos(self) -> list[Evento]:
        dtos = db.session.query(self.fabrica_eventos.dto()).all()
        return [self.fabrica_eventos.crear_objeto(dto, MapeadorEvento()) for dto in dtos]

    def agregar(self, entity: Evento):
        dto = self.fabrica_eventos.crear_objeto(entity, MapeadorEvento())
        db.session.add(dto)

    def actualizar(self, entity: Evento):
        dto = self.fabrica_eventos.crear_objeto(entity, MapeadorEvento())
        db.session.merge(dto)

    def eliminar(self, entity_id: UUID):
        dto = db.session.query(self.fabrica_eventos.dto()).filter_by(id=str(entity_id)).first()
        if dto:
            db.session.delete(dto)


class RepositorioMediosMarketingPostgres(RepositorioMediosMarketing):
    def __init__(self):
        self._fabrica_medios: FabricaMediosMarketing = FabricaMediosMarketing()

    @property
    def fabrica_medios(self):
        return self._fabrica_medios

    def obtener_por_id(self, id: UUID) -> MedioMarketing:
        dto = db.session.query(self.fabrica_medios.dto()).filter_by(id=str(id)).first()
        if dto:
            return self.fabrica_medios.crear_objeto(dto, MapeadorMedioMarketing())
        return None

    def obtener_todos(self) -> list[MedioMarketing]:
        dtos = db.session.query(self.fabrica_medios.dto()).all()
        return [self.fabrica_medios.crear_objeto(dto, MapeadorMedioMarketing()) for dto in dtos]

    def agregar(self, entity: MedioMarketing):
        print("a")
        print("a")
        print("a")
        print("a")
        print("a")
        print(entity.__class__)
        print(entity)
        dto = self.fabrica_medios.crear_objeto(entity, MapeadorMedioMarketing())
        print("1")
        print("1")
        print("1")
        print("1")
        db.session.add(dto)

    def actualizar(self, entity: MedioMarketing):
        dto = self.fabrica_medios.crear_objeto(entity, MapeadorMedioMarketing())
        db.session.merge(dto)

    def eliminar(self, entity_id: UUID):
        dto = db.session.query(self.fabrica_medios.dto()).filter_by(id=str(entity_id)).first()
        if dto:
            db.session.delete(dto)


class RepositorioPublicacionesPostgres(RepositorioPublicaciones):
    def __init__(self):
        self._fabrica_publicaciones: FabricaPublicaciones = FabricaPublicaciones()

    @property
    def fabrica_publicaciones(self):
        return self._fabrica_publicaciones

    def obtener_por_id(self, id: UUID) -> Publicacion:
        dto = db.session.query(self.fabrica_publicaciones.dto()).filter_by(id=str(id)).first()
        if dto:
            return self.fabrica_publicaciones.crear_objeto(dto, MapeadorPublicacion())
        return None

    def obtener_todos(self) -> list[Publicacion]:
        dtos = db.session.query(self.fabrica_publicaciones.dto()).all()
        return [self.fabrica_publicaciones.crear_objeto(dto, MapeadorPublicacion()) for dto in dtos]

    def agregar(self, entity: Publicacion):
        dto = self.fabrica_publicaciones.crear_objeto(entity, MapeadorPublicacion())
        db.session.add(dto)

    def actualizar(self, entity: Publicacion):
        dto = self.fabrica_publicaciones.crear_objeto(entity, MapeadorPublicacion())
        db.session.merge(dto)

    def eliminar(self, entity_id: UUID):
        dto = db.session.query(self.fabrica_publicaciones.dto()).filter_by(id=str(entity_id)).first()
        if dto:
            db.session.delete(dto)
