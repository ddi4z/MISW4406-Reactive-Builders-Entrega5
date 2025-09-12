"""Repositorios para el manejo de persistencia de objetos de dominio en la capa de infraestructura
del dominio de Asociaciones Estratégicas
"""

from asociaciones_estrategicas.config.db import db
from asociaciones_estrategicas.modulos.asociaciones.dominio.repositorios import (
    RepositorioAsociacionEstrategica,
    RepositorioEventosAsociacionEstrategica
)
from asociaciones_estrategicas.modulos.asociaciones.dominio.entidades import AsociacionEstrategica
from asociaciones_estrategicas.modulos.asociaciones.dominio.fabricas import FabricaAsociacionesEstrategicas
from .dto import AsociacionEstrategica as AsociacionDTO, EventosAsociacion
from .mapeadores import MapeadorAsociacionEstrategica, MapeadorEventosAsociacionEstrategica

from uuid import UUID
from pulsar.schema import JsonSchema


class RepositorioAsociacionesSQLAlchemy(RepositorioAsociacionEstrategica):

    def __init__(self):
        self._fabrica = FabricaAsociacionesEstrategicas()

    @property
    def fabrica(self):
        return self._fabrica

    def obtener_por_id(self, id: UUID) -> AsociacionEstrategica:
        asociacion_dto = db.session.query(AsociacionDTO).filter_by(id=str(id)).one()
        return self.fabrica.crear_objeto(asociacion_dto, MapeadorAsociacionEstrategica())

    def obtener_todos(self) -> list[AsociacionEstrategica]:
        asociaciones_dto = db.session.query(AsociacionDTO).all()
        return [self.fabrica.crear_objeto(dto, MapeadorAsociacionEstrategica()) for dto in asociaciones_dto]

    def agregar(self, asociacion: AsociacionEstrategica):
        asociacion_dto = self.fabrica.crear_objeto(asociacion, MapeadorAsociacionEstrategica())
        db.session.add(asociacion_dto)

    def actualizar(self, asociacion: AsociacionEstrategica):
        # TODO: implementar update en SQLAlchemy si lo necesitas
        raise NotImplementedError

    def eliminar(self, asociacion_id: UUID):
        # TODO: implementar delete en SQLAlchemy si lo necesitas
        raise NotImplementedError


class RepositorioEventosAsociacionesSQLAlchemy(RepositorioEventosAsociacionEstrategica):

    def __init__(self):
        self._fabrica = FabricaAsociacionesEstrategicas()

    @property
    def fabrica(self):
        return self._fabrica

    def obtener_por_id(self, id: UUID):
        evento_dto = db.session.query(EventosAsociacion).filter_by(id=str(id)).one()
        return self.fabrica.crear_objeto(evento_dto, MapeadorEventosAsociacionEstrategica())

    def obtener_todos(self):
        raise NotImplementedError

    def agregar(self, evento):
        evento_integracion = self.fabrica.crear_objeto(evento, MapeadorEventosAsociacionEstrategica())

        parser_payload = JsonSchema(evento_integracion.data.__class__)
        json_str = parser_payload.encode(evento_integracion.data)

        evento_dto = EventosAsociacion()
        evento_dto.id = str(evento.id)
        evento_dto.id_entidad = str(evento.id_asociacion)
        evento_dto.fecha_evento = evento.fecha_creacion
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
