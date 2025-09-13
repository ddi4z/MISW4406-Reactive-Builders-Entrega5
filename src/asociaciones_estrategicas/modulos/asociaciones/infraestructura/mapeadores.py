""" Mapeadores para la capa de infrastructura del dominio de vuelos

En este archivo usted encontrará los diferentes mapeadores
encargados de la transformación entre formatos de dominio y DTOs

"""

from asociaciones_estrategicas.seedwork.dominio.repositorios import Mapeador
from asociaciones_estrategicas.seedwork.infraestructura.utils import unix_time_millis
from asociaciones_estrategicas.modulos.asociaciones.dominio.objetos_valor import TipoAsociacion, PeriodoVigencia    
from asociaciones_estrategicas.modulos.asociaciones.dominio.entidades import AsociacionEstrategica
from asociaciones_estrategicas.modulos.asociaciones.dominio.eventos import AsociacionCreada, AsociacionFinalizada, EventoAsociacionEstrategica

from .dto import AsociacionEstrategica as AsociacionDTO
from .dto import EventosAsociacion
from .excepciones import NoExisteImplementacionParaTipoFabricaExcepcion
from pulsar.schema import *
from uuid import UUID


# =======================
# Eventos
# =======================

class MapeadorEventosAsociacionEstrategica(Mapeador):

    versions = ("v1",)
    LATEST_VERSION = versions[0]

    def __init__(self):
        self.router = {
            AsociacionCreada: self._entidad_a_asociacion_creada,
            AsociacionFinalizada: self._entidad_a_asociacion_finalizada,
        }

    def obtener_tipo(self) -> type:
        return EventoAsociacionEstrategica.__class__

    def es_version_valida(self, version):
        return version in self.versions

    def _entidad_a_asociacion_creada(self, entidad: AsociacionCreada, version=LATEST_VERSION):
        def v1(evento):
            from .schema.v1.eventos import AsociacionCreadaPayload, EventoAsociacionCreada
            from asociaciones_estrategicas.seedwork.infraestructura.utils import unix_time_millis

            payload = AsociacionCreadaPayload(
                id_asociacion=str(evento.id_asociacion),
                id_marca=str(evento.id_marca),
                id_socio=str(evento.id_socio),
                tipo=str(evento.tipo),
                descripcion=evento.descripcion,                              # ✅
                fecha_inicio=int(unix_time_millis(evento.fecha_inicio)),     # ✅
                fecha_fin=int(unix_time_millis(evento.fecha_fin)),           # ✅
                fecha_creacion=int(unix_time_millis(evento.fecha_creacion))
            )

            evento_integracion = EventoAsociacionCreada(id=str(evento.id_asociacion))
            evento_integracion.time = int(unix_time_millis(evento.fecha_creacion))
            evento_integracion.specversion = str(version)
            evento_integracion.type = "AsociacionCreada"
            evento_integracion.datacontenttype = "AVRO"
            evento_integracion.service_name = "asociaciones"
            evento_integracion.data = payload

            return evento_integracion

        if not self.es_version_valida(version):
            raise Exception(f"No se sabe procesar la version {version}")

        return v1(entidad)


    def _entidad_a_asociacion_finalizada(self, entidad: AsociacionFinalizada, version=LATEST_VERSION):
        def v1(evento):
            from .schema.v1.eventos import AsociacionFinalizadaPayload, EventoAsociacionFinalizada

            payload = AsociacionFinalizadaPayload(
                id_asociacion=str(evento.id_asociacion),
                fecha_actualizacion=int(unix_time_millis(evento.fecha_actualizacion))
            )

            evento_integracion = EventoAsociacionFinalizada(id=str(evento.id_asociacion))
            evento_integracion.time = int(unix_time_millis(evento.fecha_actualizacion))
            evento_integracion.specversion = str(version)
            evento_integracion.type = "AsociacionFinalizada"
            evento_integracion.datacontenttype = "AVRO"
            evento_integracion.service_name = "asociaciones"
            evento_integracion.data = payload

            return evento_integracion

        if not self.es_version_valida(version):
            raise Exception(f"No se sabe procesar la version {version}")

        return v1(entidad)

    def entidad_a_dto(self, entidad: EventoAsociacionEstrategica, version=LATEST_VERSION):
        if not entidad:
            raise NoExisteImplementacionParaTipoFabricaExcepcion
        func = self.router.get(entidad.__class__, None)
        if not func:
            raise NoExisteImplementacionParaTipoFabricaExcepcion
        return func(entidad, version=version)

    def dto_a_entidad(self, dto: EventosAsociacion, version=LATEST_VERSION):
        # TODO: implementar si necesitas reconstruir evento desde la BD
        raise NotImplementedError


# =======================
# Agregado raíz
# =======================

class MapeadorAsociacionEstrategica(Mapeador):

    def obtener_tipo(self) -> type:
        return AsociacionEstrategica.__class__

    def entidad_a_dto(self, entidad: AsociacionEstrategica) -> AsociacionDTO:
        dto = AsociacionDTO()
        dto.id = str(entidad.id)
        dto.id_marca = str(entidad.id_marca)
        dto.id_socio = str(entidad.id_socio)
        dto.tipo = entidad.tipo.value
        dto.descripcion = entidad.descripcion
        dto.fecha_inicio = entidad.vigencia.fecha_inicio
        dto.fecha_fin = entidad.vigencia.fecha_fin
        dto.fecha_creacion = entidad.fecha_creacion
        dto.fecha_actualizacion = entidad.fecha_actualizacion
        return dto

    def dto_a_entidad(self, dto: AsociacionDTO) -> AsociacionEstrategica:
        asociacion = AsociacionEstrategica(
            #id = UUID(dto.id),
            id_marca=UUID(dto.id_marca),
            id_socio=UUID(dto.id_socio),
            tipo=TipoAsociacion(dto.tipo),
            descripcion=dto.descripcion,
            vigencia=PeriodoVigencia(dto.fecha_inicio, dto.fecha_fin)
        )
        
        # Forzar a que conserve el id correcto
        asociacion._id = UUID(dto.id)

        asociacion.fecha_creacion = dto.fecha_creacion
        asociacion.fecha_actualizacion = dto.fecha_actualizacion
        return asociacion


