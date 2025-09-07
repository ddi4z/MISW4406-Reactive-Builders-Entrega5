from aeroalpes.modulos.externo.dominio.entidades import Evento, MedioMarketing, Plataforma, Publicacion, Publicacion
from aeroalpes.modulos.externo.aplicacion.dto import EventoDTO, PublicacionDTO
from aeroalpes.seedwork.aplicacion.dto import Mapeador as AppMap
from aeroalpes.seedwork.dominio.repositorios import Mapeador as RepMap
from .dto import MedioMarketingDTO, PlataformaDTO

from datetime import datetime

class MapeadorEventoDTOJson(AppMap):    
    def externo_a_dto(self, externo: dict) -> EventoDTO:
        evento_dto = EventoDTO()
        evento_dto.fecha_creacion = externo.get('fecha_creacion')
        evento_dto.fecha_actualizacion = externo.get('fecha_actualizacion')
        evento_dto.id = externo.get('id')

        return evento_dto

    def dto_a_externo(self, dto: EventoDTO) -> dict:
        return dto.__dict__

class MapeadorEvento(RepMap):
    _FORMATO_FECHA = '%Y-%m-%dT%H:%M:%SZ'

    def obtener_tipo(self) -> type:
        return Evento.__class__

    def entidad_a_dto(self, entidad: Evento) -> EventoDTO:

        fecha_creacion = entidad.fecha_creacion.strftime(self._FORMATO_FECHA)
        fecha_actualizacion = entidad.fecha_actualizacion.strftime(self._FORMATO_FECHA)
        _id = str(entidad.id)


        return EventoDTO(fecha_creacion, fecha_actualizacion, _id)

    def dto_a_entidad(self, dto: EventoDTO) -> Evento:
        evento = Evento()
        evento.fecha_creacion = datetime.strptime(dto.fecha_creacion, self._FORMATO_FECHA)
        evento.fecha_actualizacion = datetime.strptime(dto.fecha_actualizacion, self._FORMATO_FECHA)
        evento.id = int(dto.id)

        return evento
    
    
class MapeadorPublicacionDTOJson(AppMap):    
    def externo_a_dto(self, externo: dict) -> EventoDTO:
        publicacion_dto = PublicacionDTO()
        publicacion_dto.fecha_creacion = externo.get('fecha_creacion')
        publicacion_dto.fecha_actualizacion = externo.get('fecha_actualizacion')
        publicacion_dto.id = externo.get('id')
        publicacion_dto.tipo_publicacion = externo.get('tipo_publicacion')
        return publicacion_dto

    def dto_a_externo(self, dto: PublicacionDTO) -> dict:
        return dto.__dict__

class MapeadorPublicacion(RepMap):
    _FORMATO_FECHA = '%Y-%m-%dT%H:%M:%SZ'

    def obtener_tipo(self) -> type:
        return Publicacion.__class__

    def entidad_a_dto(self, entidad: Publicacion) -> PublicacionDTO:

        fecha_creacion = entidad.fecha_creacion.strftime(self._FORMATO_FECHA)
        fecha_actualizacion = entidad.fecha_actualizacion.strftime(self._FORMATO_FECHA)
        _id = str(entidad.id)


        return PublicacionDTO(fecha_creacion, fecha_actualizacion, _id)

    def dto_a_entidad(self, dto: PublicacionDTO) -> Publicacion:
        publicacion = Publicacion()
        publicacion.fecha_creacion = datetime.strptime(dto.fecha_creacion, self._FORMATO_FECHA)
        publicacion.fecha_actualizacion = datetime.strptime(dto.fecha_actualizacion, self._FORMATO_FECHA)
        publicacion.id = int(dto.id)

        return publicacion


class MapeadorPlataformaDTOJson(AppMap):    
    def externo_a_dto(self, externo: dict) -> PlataformaDTO:
        plataforma_dto = PlataformaDTO()
        plataforma_dto.fecha_creacion = externo.get('fecha_creacion')
        plataforma_dto.id = externo.get('id')
        plataforma_dto.tipo_plataforma = externo.get('tipo_plataforma')
        return plataforma_dto

    def dto_a_externo(self, dto: PlataformaDTO) -> dict:
        return dto.__dict__

class MapeadorPlataforma(RepMap):
    _FORMATO_FECHA = '%Y-%m-%dT%H:%M:%SZ'

    def obtener_tipo(self) -> type:
        return Plataforma.__class__

    def entidad_a_dto(self, entidad: Plataforma) -> PlataformaDTO:

        fecha_creacion = entidad.fecha_creacion.strftime(self._FORMATO_FECHA)
        fecha_actualizacion = entidad.fecha_actualizacion.strftime(self._FORMATO_FECHA)
        _id = str(entidad.id)


        return PlataformaDTO(fecha_creacion, fecha_actualizacion, _id)

    def dto_a_entidad(self, dto: PlataformaDTO) -> Plataforma:
        plataforma = Plataforma()
        plataforma.fecha_creacion = datetime.strptime(dto.fecha_creacion, self._FORMATO_FECHA)
        plataforma.fecha_actualizacion = datetime.strptime(dto.fecha_actualizacion, self._FORMATO_FECHA)
        plataforma.id = int(dto.id)

        return plataforma
    
    
class MapeadorMedioMarketingDTOJson(AppMap):    
    def externo_a_dto(self, externo: dict) -> MedioMarketingDTO:
        medio_dto = MedioMarketingDTO()
        medio_dto.fecha_creacion = externo.get('fecha_creacion')
        medio_dto.id = externo.get('id')
        medio_dto.tipo_medio = externo.get('tipo_medio')
        return medio_dto

    def dto_a_externo(self, dto: MedioMarketingDTO) -> dict:
        return dto.__dict__

class MapeadorMedioMarketing(RepMap):
    _FORMATO_FECHA = '%Y-%m-%dT%H:%M:%SZ'

    def obtener_tipo(self) -> type:
        return MedioMarketing.__class__

    def entidad_a_dto(self, entidad: MedioMarketing) -> MedioMarketingDTO:

        fecha_creacion = entidad.fecha_creacion.strftime(self._FORMATO_FECHA)
        fecha_actualizacion = entidad.fecha_actualizacion.strftime(self._FORMATO_FECHA)
        _id = str(entidad.id)


        return PlataformaDTO(fecha_creacion, fecha_actualizacion, _id)

    def dto_a_entidad(self, dto: MedioMarketingDTO) -> MedioMarketing:
        medio = MedioMarketing()
        medio.fecha_creacion = datetime.strptime(dto.fecha_creacion, self._FORMATO_FECHA)
        medio.fecha_actualizacion = datetime.strptime(dto.fecha_actualizacion, self._FORMATO_FECHA)
        medio.id = int(dto.id)

        return medio