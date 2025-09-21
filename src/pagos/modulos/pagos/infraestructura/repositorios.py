from pagos.config.db import SessionLocal
from pagos.modulos.pagos.dominio.entidades import Pago
from pagos.modulos.pagos.dominio.fabricas import FabricaPagos
from pagos.modulos.pagos.dominio.repositorios import RepositorioPagos
from pagos.modulos.pagos.infraestructura.dto import PagoDTO
from .mapeadores import MapeadorPago
from uuid import UUID


class RepositorioPagosPostgres(RepositorioPagos):
    def __init__(self):
        super().__init__()
        self._fabrica_pagos = FabricaPagos()
        self._session = SessionLocal() 

    @property
    def fabrica_pagos(self):
        return self._fabrica_pagos

    def obtener_por_id(self, id: UUID) -> Pago | None:
        dto = self._session.query(PagoDTO).filter_by(id=str(id)).first()
        if dto:
            return self._fabrica_pagos.crear_objeto(dto, MapeadorPago())
        return None

    def obtener_todos(self) -> list[Pago]:
        dtos = self._session.query(PagoDTO).all()
        return [self._fabrica_pagos.crear_objeto(dto, MapeadorPago()) for dto in dtos]

    def agregar(self, entity: Pago):
        dto = self._fabrica_pagos.crear_objeto(entity, MapeadorPago())
        self._session.add(dto)
        self._session.commit()

    def actualizar(self, entity: Pago):
        dto = self._fabrica_pagos.crear_objeto(entity, MapeadorPago())
        self._session.merge(dto)
        self._session.commit()

    def eliminar(self, entity_id: UUID):
        dto = self._session.query(PagoDTO).filter_by(id=str(entity_id)).first()
        if dto:
            self._session.delete(dto)
            self._session.commit()

    def revertir(self, entity_id: UUID):
        dto = self._session.query(PagoDTO).filter_by(id=str(entity_id)).first()
        if not dto:
            return None
        dto.estado = "REVERTIDO"
        self._session.commit()
        self._session.refresh(dto)
        return self._fabrica_pagos.crear_objeto(dto, MapeadorPago())
