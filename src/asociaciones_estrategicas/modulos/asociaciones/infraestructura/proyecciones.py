from asociaciones_estrategicas.seedwork.infraestructura.proyecciones import Proyeccion, ProyeccionHandler
from asociaciones_estrategicas.seedwork.infraestructura.proyecciones import ejecutar_proyeccion as proyeccion
from asociaciones_estrategicas.seedwork.infraestructura.utils import millis_a_datetime
from asociaciones_estrategicas.modulos.asociaciones.infraestructura.dto import AsociacionesAnalitica, Asociacion as AsociacionDTO
from asociaciones_estrategicas.modulos.asociaciones.dominio.entidades import AsociacionEstrategica
from asociaciones_estrategicas.modulos.asociaciones.dominio.objetos_valor import PeriodoVigencia, TipoAsociacion
from asociaciones_estrategicas.modulos.asociaciones.infraestructura.mapeadores import MapeadorAsociacionEstrategica
from asociaciones_estrategicas.config.db import db

import logging
import traceback
from abc import ABC, abstractmethod


# =====================
# Base
# =====================

class ProyeccionAsociacion(Proyeccion, ABC):
    @abstractmethod
    def ejecutar(self):
        ...


# =====================
# Analítica
# =====================

class ProyeccionAsociacionesTotales(ProyeccionAsociacion):
    ADD = 1
    DELETE = 2

    def __init__(self, fecha_creacion, operacion):
        self.fecha_creacion = millis_a_datetime(fecha_creacion)
        self.operacion = operacion

    def ejecutar(self, db=None):
        if not db:
            logging.error("ERROR: DB del app no puede ser nula")
            return

        record = db.session.query(AsociacionesAnalitica).filter_by(
            fecha_creacion=self.fecha_creacion.date()
        ).one_or_none()

        if record and self.operacion == self.ADD:
            record.total += 1
        elif record and self.operacion == self.DELETE:
            record.total -= 1
            record.total = max(record.total, 0)
        else:
            db.session.add(
                AsociacionesAnalitica(
                    fecha_creacion=self.fecha_creacion.date(), total=1
                )
            )

        db.session.commit()


# =====================
# Lista de asociaciones
# =====================

class ProyeccionAsociacionesLista(ProyeccionAsociacion):
    def __init__(self, id_asociacion, id_marca, id_socio, tipo, descripcion, fecha_inicio, fecha_fin, fecha_creacion, fecha_actualizacion):
        self.id_asociacion = id_asociacion
        self.id_marca = id_marca
        self.id_socio = id_socio
        self.tipo = tipo
        self.descripcion = descripcion
        self.fecha_inicio = millis_a_datetime(fecha_inicio)
        self.fecha_fin = millis_a_datetime(fecha_fin)
        self.fecha_creacion = millis_a_datetime(fecha_creacion)
        self.fecha_actualizacion = millis_a_datetime(fecha_actualizacion)

    def ejecutar(self, db=None):
        if not db:
            logging.error("ERROR: DB del app no puede ser nula")
            return

        # Usamos DTO directamente para la tabla asociaciones
        asociacion_dto = db.session.query(AsociacionDTO).filter_by(id=str(self.id_asociacion)).one_or_none()

        if asociacion_dto:
            # actualizar
            asociacion_dto.id_marca = str(self.id_marca)
            asociacion_dto.id_socio = str(self.id_socio)
            asociacion_dto.tipo = str(self.tipo)
            asociacion_dto.descripcion = self.descripcion
            asociacion_dto.fecha_inicio = self.fecha_inicio
            asociacion_dto.fecha_fin = self.fecha_fin
            asociacion_dto.fecha_creacion = self.fecha_creacion
            asociacion_dto.fecha_actualizacion = self.fecha_actualizacion
        else:
            # insertar
            nueva_asociacion = AsociacionDTO(
                id=str(self.id_asociacion),
                id_marca=str(self.id_marca),
                id_socio=str(self.id_socio),
                tipo=str(self.tipo),
                descripcion=self.descripcion,
                fecha_inicio=self.fecha_inicio,
                fecha_fin=self.fecha_fin,
                fecha_creacion=self.fecha_creacion,
                fecha_actualizacion=self.fecha_actualizacion,
            )
            db.session.add(nueva_asociacion)

        db.session.commit()


# =====================
# Handler
# =====================

class ProyeccionAsociacionHandler(ProyeccionHandler):
    def handle(self, proyeccion: ProyeccionAsociacion):
        from asociaciones_estrategicas.config.db import db
        proyeccion.ejecutar(db=db)


# =====================
# Registro
# =====================

@proyeccion.register(ProyeccionAsociacionesLista)
@proyeccion.register(ProyeccionAsociacionesTotales)
def ejecutar_proyeccion_asociacion(proyeccion, app=None):
    if not app:
        logging.error("ERROR: Contexto del app no puede ser nulo")
        return
    try:
        with app.app_context():
            handler = ProyeccionAsociacionHandler()
            handler.handle(proyeccion)
    except:
        traceback.print_exc()
        logging.error("ERROR: Persistiendo proyección de asociaciones!")
