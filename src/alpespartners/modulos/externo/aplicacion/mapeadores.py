from alpespartners.modulos.externo.dominio.entidades import Evento, MedioMarketing, Publicacion, Publicacion
import alpespartners.modulos.externo.dominio.objetos_valor as ov
from alpespartners.modulos.externo.aplicacion.dto import EventoDTO, PublicacionDTO
from alpespartners.seedwork.aplicacion.dto import Mapeador as AppMap
from alpespartners.seedwork.dominio.repositorios import Mapeador as RepMap
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
        fecha_creacion = externo.get('fecha_creacion')
        fecha_actualizacion = externo.get('fecha_actualizacion')
        id = externo.get('id')
        return PublicacionDTO(fecha_creacion=fecha_creacion, fecha_actualizacion=fecha_actualizacion, id=id)

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
    
class MapeadorMedioMarketingDTOJson(AppMap):    
    def externo_a_dto(self, externo: dict) -> MedioMarketingDTO:
    
        fecha_creacion = externo.get('fecha_creacion')
        fecha_actualizacion = externo.get('fecha_actualizacion')
        id = externo.get('id')
        return MedioMarketingDTO(fecha_creacion, fecha_actualizacion, id)

    def dto_a_externo(self, dto: MedioMarketingDTO) -> dict:
        return dto.__dict__

class MapeadorMedioMarketing(RepMap):
    _FORMATO_FECHA = '%Y-%m-%dT%H:%M:%SZ'

    def obtener_tipo(self) -> type:
        return MedioMarketing.__class__
    
    def plataforma_a_dict(self, plataforma):
        if not plataforma:
            return dict(nombre=None)
        
        return dict(     
            nombre=plataforma.nombre
        )


    def entidad_a_dto(self, entidad: MedioMarketing) -> MedioMarketingDTO:

        fecha_creacion = entidad.fecha_creacion.strftime(self._FORMATO_FECHA)
        fecha_actualizacion = entidad.fecha_actualizacion.strftime(self._FORMATO_FECHA)
        _id = str(entidad.id)
        plataforma = self.plataforma_a_dict(entidad.plataforma)


        return MedioMarketingDTO(fecha_creacion, fecha_actualizacion, _id, plataforma)

    def dto_a_entidad(self, dto: MedioMarketingDTO) -> MedioMarketing:
        fecha_creacion = datetime.strptime(dto.fecha_creacion, self._FORMATO_FECHA)
        fecha_actualizacion = datetime.strptime(dto.fecha_actualizacion, self._FORMATO_FECHA)
        _id = int(dto.id)
        plataforma = ov.Plataforma(nombre=dto.plataforma.nombre)

        return MedioMarketing(fecha_creacion=fecha_creacion, fecha_actualizacion=fecha_actualizacion, id=_id, plataforma=plataforma)