from pagos.config.db import db
from pagos.modulos.pagos.dominio.entidades import Pago
from pagos.modulos.pagos.dominio.fabricas import FabricaPagos
from pagos.modulos.pagos.dominio.repositorios import RepositorioEventosPagos, RepositorioPagos
from pagos.modulos.pagos.infraestructura.dto import EventosPagoDTO, PagoDTO
from .mapeadores import MapeadorEventosPago, MapeadorPago
from uuid import UUID
from pulsar.schema import JsonSchema


class RepositorioPagosPostgres(RepositorioPagos):
    def __init__(self):
        super().__init__()
        self._fabrica_pagos = FabricaPagos()

    @property
    def fabrica_pagos(self):
        return self._fabrica_pagos

    def obtener_por_id(self, id: UUID) -> Pago | None:
        dto = db.session.query(PagoDTO).filter_by(id=str(id)).first()
        if dto:
            return self._fabrica_pagos.crear_objeto(dto, MapeadorPago())
        return None

    def obtener_todos(self) -> list[Pago]:
        dtos = db.session.query(PagoDTO).all()
        return [self._fabrica_pagos.crear_objeto(dto, MapeadorPago()) for dto in dtos]

    def agregar(self, entity: Pago):
        dto = self._fabrica_pagos.crear_objeto(entity, MapeadorPago())
        db.session.add(dto)


    def actualizar(self, entity: Pago):
        dto = self._fabrica_pagos.crear_objeto(entity, MapeadorPago())
        db.session.merge(dto)

    def eliminar(self, entity_id: UUID):
        dto = db.session.query(PagoDTO).filter_by(id=str(entity_id)).first()
        if dto:
            db.session.delete(dto)
        

    def revertir(self, entity_id: UUID):
        dto = db.session.query(PagoDTO).filter_by(id=str(entity_id)).first()
        if not dto:
            return None
        dto.estado = "REVERTIDO"
        db.session.refresh(dto)
        return self._fabrica_pagos.crear_objeto(dto, MapeadorPago())


class RepositorioEventosPagosPostgres(RepositorioEventosPagos):

    def __init__(self):
        self._fabrica = FabricaPagos()

    @property
    def fabrica(self):
        return self._fabrica

    def obtener_por_id(self, id: UUID):
        evento_dto = db.session.query(EventosPagoDTO).filter_by(id=str(id)).one()
        return self.fabrica.crear_objeto(evento_dto, MapeadorEventosPago())

    def obtener_todos(self):
        raise NotImplementedError

    def agregar(self, evento):
        evento_integracion = self.fabrica.crear_objeto(evento, MapeadorEventosPago())

        parser_payload = JsonSchema(evento_integracion.data.__class__)
        json_str = parser_payload.encode(evento_integracion.data)

        evento_dto = EventosPagoDTO()
        evento_dto.id = str(evento.id)
        
        
        evento_dto.id_entidad = str(evento.id_pago)
        
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
