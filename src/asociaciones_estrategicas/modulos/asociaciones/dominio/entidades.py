"""Entidades del dominio de vuelos

En este archivo usted encontrará las entidades del dominio de vuelos

"""

from __future__ import annotations
from dataclasses import dataclass, field
import datetime
import uuid
from asociaciones_estrategicas.seedwork.dominio.entidades import AgregacionRaiz
from asociaciones_estrategicas.modulos.asociaciones.dominio.objetos_valor import PeriodoVigencia, TipoAsociacion
from asociaciones_estrategicas.modulos.asociaciones.dominio.eventos import AsociacionCreada, AsociacionFinalizada, OnboardingFallido, OnboardingIniciado

@dataclass
class AsociacionEstrategica(AgregacionRaiz):
    id_marca: uuid.UUID = field(default=None)
    id_socio: uuid.UUID = field(default=None)
    tipo: TipoAsociacion = field(default=TipoAsociacion.PROGRAMA_AFILIADOS)
    descripcion: str = field(default="")
    vigencia: PeriodoVigencia = None

    def crear_asociacion(self, asociacion_estrategica: AsociacionEstrategica, in_id_correlacion: str):
        try:
            self.id_marca = asociacion_estrategica.id_marca
            self.id_socio = asociacion_estrategica.id_socio
            self.tipo = asociacion_estrategica.tipo
            self.vigencia = asociacion_estrategica.vigencia
            self.descripcion = asociacion_estrategica.descripcion
            self.fecha_creacion = datetime.datetime.now()

            self.agregar_evento(OnboardingIniciado(
                id_correlacion=in_id_correlacion,
                id_asociacion=self.id,
                id_marca=self.id_marca,
                id_socio=self.id_socio,
                tipo=self.tipo.value,
                descripcion=self.descripcion,
                fecha_inicio=self.vigencia.fecha_inicio,
                fecha_fin=self.vigencia.fecha_fin,
                fecha_creacion=self.fecha_creacion
            ))

        except Exception as e:
            self.agregar_evento(OnboardingFallido(
                id_correlacion=in_id_correlacion,
                id_asociacion=self.id,
                motivo=str(e)
            ))
            raise


    def finalizar_asociacion(self):
        self.fecha_actualizacion = datetime.datetime.now()

        # Publicar evento
        self.agregar_evento(AsociacionFinalizada(
                id_asociacion=self.id,
                fecha_actualizacion=self.fecha_actualizacion
        ))
