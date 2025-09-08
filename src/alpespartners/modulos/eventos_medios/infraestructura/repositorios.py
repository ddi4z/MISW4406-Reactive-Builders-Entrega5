from alpespartners.config.db import db
from alpespartners.modulos.eventos_medios.dominio.repositorios import (
    RepositorioEventos,
    RepositorioMediosMarketing,
)
from alpespartners.modulos.eventos_medios.dominio.entidades import Evento, MedioMarketing, Publicacion
from alpespartners.modulos.eventos_medios.infraestructura.dto import EventoDTO, MedioMarketingDTO
from .mapeadores import (
    MapeadorMedioMarketing,
    MapeadorPublicacion,
    MapeadorEvento
)
from alpespartners.modulos.eventos_medios.dominio.fabricas import (
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
        dto = db.session.query(EventoDTO).filter_by(id=str(id)).first()
        if dto:
            return self.fabrica_eventos.crear_objeto(dto, MapeadorEvento())
        return None

    def obtener_todos(self) -> list[Evento]:
        dtos = db.session.query(EventoDTO).all()
        return [self.fabrica_eventos.crear_objeto(dto, MapeadorEvento()) for dto in dtos]

    def agregar(self, entity: Evento):
        dto = self.fabrica_eventos.crear_objeto(entity, MapeadorEvento())
        db.session.add(dto)

    def actualizar(self, entity: Evento):
        dto = self.fabrica_eventos.crear_objeto(entity, MapeadorEvento())
        db.session.merge(dto)

    def eliminar(self, entity_id: UUID):
        dto = db.session.query(EventoDTO).filter_by(id=str(entity_id)).first()
        if dto:
            db.session.delete(dto)


class RepositorioMediosMarketingPostgres(RepositorioMediosMarketing):
    def __init__(self):
        self._fabrica_medios: FabricaMediosMarketing = FabricaMediosMarketing()

    @property
    def fabrica_medios(self):
        return self._fabrica_medios

    def obtener_por_id(self, id: UUID) -> MedioMarketing:
        dto = db.session.query(MedioMarketingDTO).filter_by(id=str(id)).first()
        if dto:
            return self.fabrica_medios.crear_objeto(dto, MapeadorMedioMarketing())
        return None

    def obtener_todos(self) -> list[MedioMarketing]:
        dtos = db.session.query(MedioMarketingDTO).all()
        return [self.fabrica_medios.crear_objeto(dto, MapeadorMedioMarketing()) for dto in dtos]

    def agregar(self, entity: MedioMarketing):
        dto = self.fabrica_medios.crear_objeto(entity, MapeadorMedioMarketing())
        db.session.add(dto)

    def actualizar(self, entity: MedioMarketing):
        dto = self.fabrica_medios.crear_objeto(entity, MapeadorMedioMarketing())
        db.session.merge(dto)

    def eliminar(self, entity_id: UUID):
        dto = db.session.query(self.fabrica_medios.dto()).filter_by(id=str(entity_id)).first()
        if dto:
            db.session.delete(dto)

