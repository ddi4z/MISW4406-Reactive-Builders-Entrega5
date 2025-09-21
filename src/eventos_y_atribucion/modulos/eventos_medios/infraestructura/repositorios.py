from eventos_y_atribucion.config.db import db
from eventos_y_atribucion.modulos.eventos_medios.dominio.repositorios import (
    RepositorioEventos,
    RepositorioEventosEventos,
    RepositorioMediosMarketing,
)
from eventos_y_atribucion.modulos.eventos_medios.dominio.entidades import Evento, MedioMarketing, Publicacion
from eventos_y_atribucion.modulos.eventos_medios.infraestructura.dto import EventoDTO, EventosEventoDTO, MedioMarketingDTO

from .mapeadores import (
    MapeadorEventosEvento,
    MapeadorMedioMarketing,
    MapeadorPublicacion,
    MapeadorEvento
)
from eventos_y_atribucion.modulos.eventos_medios.dominio.fabricas import (
    FabricaMediosMarketing,
    FabricaEventos,
    FabricaPublicaciones
)
from pulsar.schema import JsonSchema
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
            
    def revertir(self, entity_id: UUID) -> Evento:
        dto = db.session.query(EventoDTO).filter_by(id=str(entity_id)).first()
        if not dto:
            return None

        dto.tipo_evento = "REVERTIDO"
        db.session.commit()
        db.session.refresh(dto)

        return self.fabrica_eventos.crear_objeto(dto, MapeadorEvento())
            


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

class RepositorioEventosEventosPostgres(RepositorioEventosEventos):

    def __init__(self):
        self._fabrica = FabricaEventos()

    @property
    def fabrica(self):
        return self._fabrica

    def obtener_por_id(self, id: UUID):
        evento_dto = db.session.query(EventosEventoDTO).filter_by(id=str(id)).one()
        return self.fabrica.crear_objeto(evento_dto, MapeadorEventosEvento())

    def obtener_todos(self):
        raise NotImplementedError

    def agregar(self, evento):
        evento_integracion = self.fabrica.crear_objeto(evento, MapeadorEventosEvento())

        parser_payload = JsonSchema(evento_integracion.data.__class__)
        json_str = parser_payload.encode(evento_integracion.data)

        evento_dto = EventosEventoDTO()
        evento_dto.id = str(evento.id)
        evento_dto.id_entidad = str(evento.id_evento)
        
        #evento_dto.fecha_evento = evento.fecha_creacion
        # 👇 Usa fecha_evento si no tiene fecha_creacion
        evento_dto.fecha_evento = getattr(evento, "fecha_creacion", None) or getattr(evento, "fecha_evento")


        evento_dto.version = str(evento_integracion.specversion)
        evento_dto.tipo_evento = evento.__class__.__name__
        evento_dto.formato_contenido = "JSON"
        evento_dto.nombre_servicio = str(evento_integracion.service_name)
        evento_dto.contenido = json_str

        db.session.add(evento_dto)

    def actualizar(self, evento):
        raise NotImplementedError

    def eliminar(self, evento_id: UUID):
        raise NotImplementedError
