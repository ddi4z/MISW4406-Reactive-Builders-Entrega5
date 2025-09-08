from alpespartners.modulos.comision_recompensa.dominio.entidades import Comision, Recompensa
import alpespartners.modulos.comision_recompensa.dominio.objetos_valor as ov
from alpespartners.seedwork.aplicacion.dto import Mapeador as AppMap
from alpespartners.seedwork.dominio.repositorios import Mapeador as RepMap
from .dto import ComisionDTO, RecompensaDTO


from datetime import datetime

class MapeadorComisionDTOJson(AppMap):    
    def externo_a_dto(self, externo: dict) -> ComisionDTO:
        fecha_creacion = externo.get('fecha_creacion')
        fecha_actualizacion = externo.get('fecha_actualizacion')
        id = externo.get('id')
        id_evento = externo.get('id_evento')
        monto_comision = externo.get('monto_comision')
        return ComisionDTO(fecha_creacion=fecha_creacion, fecha_actualizacion=fecha_actualizacion, id=id, id_evento=id_evento, valor=monto_comision["valor"])

    def dto_a_externo(self, dto: ComisionDTO) -> dict:
        return dto.__dict__

class MapeadorComision(RepMap):
    _FORMATO_FECHA = '%Y-%m-%dT%H:%M:%SZ'

    def obtener_tipo(self) -> type:
        return Comision.__class__
    

    def entidad_a_dto(self, entidad: Comision) -> Comision:

        fecha_creacion = entidad.fecha_creacion.strftime(self._FORMATO_FECHA)
        fecha_actualizacion = entidad.fecha_actualizacion.strftime(self._FORMATO_FECHA)
        _id = str(entidad.id)
        valor = entidad.valor
        id_evento = entidad.id_evento


        return Comision(fecha_creacion=fecha_creacion, fecha_actualizacion=fecha_actualizacion, id=_id, valor=valor, id_evento=id_evento)

    def dto_a_entidad(self, dto: RecompensaDTO) -> Recompensa:
        fecha_creacion = datetime.strptime(dto.fecha_creacion, self._FORMATO_FECHA)
        fecha_actualizacion = datetime.strptime(dto.fecha_actualizacion, self._FORMATO_FECHA)
        _id = dto.id
        valor = dto.valor
        id_evento = dto.id_evento

        return Comision(fecha_creacion=fecha_creacion, fecha_actualizacion=fecha_actualizacion, id=_id, monto_comision=ov.MontoComision(valor), id_evento=id_evento)

class MapeadorRecompensaDTOJson(AppMap):    
    def externo_a_dto(self, externo: dict) -> RecompensaDTO:
        fecha_creacion = externo.get('fecha_creacion')
        fecha_actualizacion = externo.get('fecha_actualizacion')
        id = externo.get('id')
        id_evento = externo.get('id_evento')
        descripcion = externo.get('descripcion')
        return RecompensaDTO(fecha_creacion=fecha_creacion, fecha_actualizacion=fecha_actualizacion, id=id, id_evento=id_evento, descripcion=descripcion)

    def dto_a_externo(self, dto: RecompensaDTO) -> dict:
        return dto.__dict__

class MapeadorRecompensa(RepMap):
    _FORMATO_FECHA = '%Y-%m-%dT%H:%M:%SZ'

    def obtener_tipo(self) -> type:
        return Recompensa.__class__

    def entidad_a_dto(self, entidad: Recompensa) -> RecompensaDTO:

        fecha_creacion = entidad.fecha_creacion.strftime(self._FORMATO_FECHA)
        fecha_actualizacion = entidad.fecha_actualizacion.strftime(self._FORMATO_FECHA)
        _id = str(entidad.id)
        descripcion = entidad.descripcion
        id_evento = entidad.id_evento


        return RecompensaDTO(fecha_creacion=fecha_creacion, fecha_actualizacion=fecha_actualizacion, id=_id, descripcion=descripcion, id_evento=id_evento)

    def dto_a_entidad(self, dto: RecompensaDTO) -> Recompensa:
        fecha_creacion = datetime.strptime(dto.fecha_creacion, self._FORMATO_FECHA)
        fecha_actualizacion = datetime.strptime(dto.fecha_actualizacion, self._FORMATO_FECHA)
        _id = dto.id
        descripcion = dto.descripcion
        id_evento = dto.id_evento

        return Recompensa(fecha_creacion=fecha_creacion, fecha_actualizacion=fecha_actualizacion, id=_id, descripcion=descripcion, id_evento=id_evento)