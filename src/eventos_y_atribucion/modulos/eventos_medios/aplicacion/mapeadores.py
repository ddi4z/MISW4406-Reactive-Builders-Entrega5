from eventos_y_atribucion.modulos.eventos_medios.dominio.entidades import Evento, InteraccionPublicacion, Lead, MedioMarketing, Publicacion, Publicacion
import eventos_y_atribucion.modulos.eventos_medios.dominio.objetos_valor as ov
from eventos_y_atribucion.modulos.eventos_medios.aplicacion.dto import EventoDTO, PublicacionDTO
from eventos_y_atribucion.seedwork.aplicacion.dto import Mapeador as AppMap
from eventos_y_atribucion.seedwork.dominio.repositorios import Mapeador as RepMap
from .dto import MedioMarketingDTO, PlataformaDTO


from datetime import datetime

class MapeadorEventoDTOJson(AppMap):    
    def externo_a_dto(self, externo: dict) -> EventoDTO:
        evento_dto = EventoDTO(
            fecha_creacion=externo.get('fecha_creacion'),
            fecha_actualizacion=externo.get('fecha_actualizacion'),
            id=externo.get('id'),
            tipo_evento=externo.get('tipo_evento'),
            id_publicacion=externo.get('id_publicacion')
        )
        return evento_dto

    def dto_a_externo(self, dto: EventoDTO) -> dict:
        return {
            "fecha_creacion": dto.fecha_creacion,
            "fecha_actualizacion": dto.fecha_actualizacion,
            "id": dto.id,
            "tipo_evento": dto.tipo_evento 
        }

class MapeadorEvento(RepMap):
    _FORMATO_FECHA = '%Y-%m-%dT%H:%M:%SZ'

    def obtener_tipo(self) -> type:
        return Evento.__class__

    def entidad_a_dto(self, entidad: Evento) -> EventoDTO:
        fecha_creacion = entidad.fecha_creacion.strftime(self._FORMATO_FECHA)
        fecha_actualizacion = entidad.fecha_actualizacion.strftime(self._FORMATO_FECHA)
        _id = entidad.id
        id_publicacion = entidad.id_publicacion

        if isinstance(entidad, Lead):
            tipo_evento = "Lead"
        elif isinstance(entidad, InteraccionPublicacion):
            tipo_evento = "InteraccionPublicacion"
        else:
            raise ValueError(f"Tipo de evento no soportado: {entidad.__class__.__name__}")

        return EventoDTO(
            fecha_creacion=fecha_creacion,
            fecha_actualizacion=fecha_actualizacion,
            id=_id,
            tipo_evento=tipo_evento,
            id_publicacion = id_publicacion
        )

    def dto_a_entidad(self, dto: EventoDTO) -> Evento:
        fecha_creacion = datetime.strptime(dto.fecha_creacion, self._FORMATO_FECHA)
        fecha_actualizacion = datetime.strptime(dto.fecha_actualizacion, self._FORMATO_FECHA)

        if dto.tipo_evento == "Lead":
            return Lead(
                id=dto.id,
                fecha_creacion=fecha_creacion,
                fecha_actualizacion=fecha_actualizacion,
                id_publicacion = dto.id_publicacion
            )
        elif dto.tipo_evento == "InteraccionPublicacion":
            return InteraccionPublicacion(
                id=dto.id,
                fecha_creacion=fecha_creacion,
                fecha_actualizacion=fecha_actualizacion,
                id_publicacion = dto.id_publicacion
            )
        else:
            raise ValueError(f"Tipo de evento no soportado en DTO: {dto.tipo_evento}")
    
    
class MapeadorPublicacionDTOJson(AppMap):    
    def externo_a_dto(self, externo: dict) -> EventoDTO:
        fecha_creacion = externo.get('fecha_creacion')
        fecha_actualizacion = externo.get('fecha_actualizacion')
        id = externo.get('id')
        id_medio_marketing = externo.get('id_medio_marketing')
        tipo_publicacion = externo.get('tipo_publicacion')
        return PublicacionDTO(fecha_creacion=fecha_creacion, fecha_actualizacion=fecha_actualizacion, id=id, id_medio_marketing=id_medio_marketing, tipo_publicacion=tipo_publicacion)

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
        
        fecha_creacion = datetime.strptime(dto.fecha_creacion, self._FORMATO_FECHA)
        fecha_actualizacion = datetime.strptime(dto.fecha_actualizacion, self._FORMATO_FECHA)
        id = dto.id
        id_medio_marketing = dto.id_medio_marketing
        tipo_publicacion = dto.tipo_publicacion

        return Publicacion(fecha_creacion = fecha_creacion, fecha_actualizacion=fecha_actualizacion, id=id, id_medio_marketing=id_medio_marketing, tipo_publicacion=tipo_publicacion)
    
class MapeadorMedioMarketingDTOJson(AppMap):    
    def externo_a_dto(self, externo: dict) -> MedioMarketingDTO:
    
        fecha_creacion = externo.get('fecha_creacion')
        fecha_actualizacion = externo.get('fecha_actualizacion')
        plataforma = externo.get('plataforma')
        id = externo.get('id')
        return MedioMarketingDTO(fecha_creacion, fecha_actualizacion, id, plataforma=plataforma)

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
        _id = dto.id
        plataforma = ov.Plataforma(nombre=dto.plataforma.nombre)

        return MedioMarketing(fecha_creacion=fecha_creacion, fecha_actualizacion=fecha_actualizacion, id=_id, plataforma=plataforma)