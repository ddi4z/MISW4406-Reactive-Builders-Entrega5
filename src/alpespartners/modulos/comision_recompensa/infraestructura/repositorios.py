from alpespartners.config.db import db
from alpespartners.modulos.comision_recompensa.dominio.repositorios import (
    RepositorioComisiones,
    RepositorioRecompensas
)
from alpespartners.modulos.comision_recompensa.dominio.entidades import Comision, Recompensa
from alpespartners.modulos.comision_recompensa.infraestructura.dto import ComisionDTO, RecompensaDTO
from .mapeadores import (
    MapeadorComision,
    MapeadorRecompensa,
)
from alpespartners.modulos.comision_recompensa.dominio.fabricas import (
    FabricaComisiones,
    FabricaRecompensas
)
from uuid import UUID


class RepositorioRecompensasPostgres(RepositorioRecompensas):
    def __init__(self):
        super().__init__()
        self._fabrica_recompensas = FabricaRecompensas()

    @property
    def fabrica_recompensas(self):
        return self._fabrica_recompensas

    def obtener_por_id(self, id: UUID) -> Recompensa:
        dto = db.session.query(RecompensaDTO).filter_by(id=str(id)).first()
        if dto:
            return self._fabrica_recompensas.crear_objeto(dto, MapeadorRecompensa())
        return None

    def obtener_todos(self) -> list[Recompensa]:
        dtos = db.session.query(RecompensaDTO).all()
        return [self._fabrica_recompensas.crear_objeto(dto, MapeadorRecompensa()) for dto in dtos]

    def agregar(self, entity: Recompensa):
        dto = self._fabrica_recompensas.crear_objeto(entity, MapeadorRecompensa())
        db.session.add(dto)

    def actualizar(self, entity: Recompensa):
        dto = self._fabrica_recompensas.crear_objeto(entity, MapeadorRecompensa())
        db.session.merge(dto)

    def eliminar(self, entity_id: UUID):
        dto = db.session.query(RecompensaDTO).filter_by(id=str(entity_id)).first()
        if dto:
            db.session.delete(dto)


class RepositorioComisionesPostgres(RepositorioComisiones):
    def __init__(self):
        self._fabrica_comisiones: FabricaComisiones = FabricaComisiones()

    @property
    def fabrica_comisiones(self):
        return self._fabrica_comisiones

    def obtener_por_id(self, id: UUID) -> Comision:
        dto = db.session.query(ComisionDTO).filter_by(id=str(id)).first()
        if dto:
            return self.fabrica_comisiones.crear_objeto(dto, MapeadorComision())
        return None

    def obtener_todos(self) -> list[Comision]:
        dtos = db.session.query(ComisionDTO).all()
        return [self.fabrica_comisiones.crear_objeto(dto, MapeadorComision()) for dto in dtos]

    def agregar(self, entity: Comision):
        dto = self.fabrica_comisiones.crear_objeto(entity, MapeadorComision())
        db.session.add(dto)

    def actualizar(self, entity: Comision):
        dto = self.fabrica_comisiones.crear_objeto(entity, MapeadorComision())
        db.session.merge(dto)

    def eliminar(self, entity_id: UUID):
        dto = db.session.query(ComisionDTO).filter_by(id=str(entity_id)).first()
        if dto:
            db.session.delete(dto)


