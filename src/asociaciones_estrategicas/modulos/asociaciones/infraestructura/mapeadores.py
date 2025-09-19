""" Mapeadores para la capa de infrastructura del dominio de vuelos

En este archivo usted encontrará los diferentes mapeadores
encargados de la transformación entre formatos de dominio y DTOs

"""

from asociaciones_estrategicas.seedwork.dominio.repositorios import Mapeador
from asociaciones_estrategicas.seedwork.infraestructura.utils import unix_time_millis
from asociaciones_estrategicas.modulos.asociaciones.dominio.objetos_valor import TipoAsociacion, PeriodoVigencia    
from asociaciones_estrategicas.modulos.asociaciones.dominio.entidades import AsociacionEstrategica
from asociaciones_estrategicas.modulos.asociaciones.dominio.eventos import AsociacionCreada, AsociacionFinalizada, EventoAsociacionEstrategica, OnboardingCancelado, OnboardingFallido, OnboardingIniciado

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
            OnboardingIniciado: self._entidad_a_onboarding_iniciado,
            OnboardingFallido: self._entidad_a_onboarding_fallido,
            OnboardingCancelado: self._entidad_a_onboarding_cancelado,
        }

    def obtener_tipo(self) -> type:
        return EventoAsociacionEstrategica.__class__

    def es_version_valida(self, version):
        return version in self.versions

    def _entidad_a_onboarding_iniciado(self, entidad: OnboardingIniciado, version=LATEST_VERSION):
        from .schema.v1.eventos import EventoAsociacion, AsociacionPayload
        payload = AsociacionPayload(
            id_correlacion=entidad.id_correlacion,
            id_asociacion=str(entidad.id_asociacion),
            id_marca=str(entidad.id_marca),
            id_socio=str(entidad.id_socio),
            tipo=str(entidad.tipo),
            descripcion=entidad.descripcion,
            fecha_inicio=int(unix_time_millis(entidad.fecha_inicio)),
            fecha_fin=int(unix_time_millis(entidad.fecha_fin)),
            fecha_creacion=int(unix_time_millis(entidad.fecha_creacion)),
        )
        evento = EventoAsociacion(id=str(entidad.id_asociacion))
        evento.time = int(unix_time_millis(entidad.fecha_creacion))
        evento.specversion = str(version)
        evento.type = "Asociacion"
        evento.estado = "OnboardingIniciado"
        evento.datacontenttype = "AVRO"
        evento.service_name = "asociaciones"
        evento.data = payload
        return evento


    def _entidad_a_onboarding_fallido(self, entidad: OnboardingFallido, version=LATEST_VERSION):
        from .schema.v1.eventos import EventoAsociacion, AsociacionPayload
        payload = AsociacionPayload(
            id_correlacion=entidad.id_correlacion,
            id_asociacion=str(entidad.id_asociacion),
            motivo=entidad.motivo,
            fecha_creacion=int(unix_time_millis(entidad.fecha_evento)),
        )
        evento = EventoAsociacion(id=str(entidad.id_asociacion))
        evento.time = int(unix_time_millis(entidad.fecha_evento))
        evento.specversion = str(version)
        evento.type = "Asociacion"
        evento.estado = "OnboardingFallido"
        evento.datacontenttype = "AVRO"
        evento.service_name = "asociaciones"
        evento.data = payload
        return evento


    def _entidad_a_onboarding_cancelado(self, entidad: OnboardingCancelado, version=LATEST_VERSION):
        from .schema.v1.eventos import EventoAsociacion, AsociacionPayload
        payload = AsociacionPayload(
            id_correlacion=entidad.id_correlacion,
            id_asociacion=str(entidad.id_asociacion),
            fecha_cancelacion=int(unix_time_millis(entidad.fecha_cancelacion)),
            fecha_creacion=int(unix_time_millis(entidad.fecha_evento)),
        )
        evento = EventoAsociacion(id=str(entidad.id_asociacion))
        evento.time = int(unix_time_millis(entidad.fecha_cancelacion))
        evento.specversion = str(version)
        evento.type = "Asociacion"
        evento.estado = "OnboardingCancelado"
        evento.datacontenttype = "AVRO"
        evento.service_name = "asociaciones"
        evento.data = payload
        return evento
  

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


