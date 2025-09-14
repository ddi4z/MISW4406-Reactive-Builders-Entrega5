from asociaciones_estrategicas.seedwork.aplicacion.dto import Mapeador as AppMap
from asociaciones_estrategicas.seedwork.dominio.repositorios import Mapeador as RepMap

from asociaciones_estrategicas.modulos.asociaciones.dominio.entidades import AsociacionEstrategica
from asociaciones_estrategicas.modulos.asociaciones.dominio.objetos_valor import PeriodoVigencia, TipoAsociacion
from .dto import AsociacionDTO, VigenciaDTO

from datetime import datetime, timezone


class MapeadorAsociacionDTOJson(AppMap):
    """Convierte JSON externo ↔ DTO de aplicación"""

    def externo_a_dto(self, externo: dict) -> AsociacionDTO:
        vigencia = None
        if "vigencia" in externo:
            vigencia = VigenciaDTO(
                fecha_inicio=externo["vigencia"].get("fecha_inicio"),
                fecha_fin=externo["vigencia"].get("fecha_fin"),
            )

        return AsociacionDTO(
            id=externo.get("id", ""),
            id_marca=externo.get("id_marca", ""),
            id_socio=externo.get("id_socio", ""),
            tipo=externo.get("tipo", ""),
            descripcion=externo.get("descripcion", ""),
            vigencia=vigencia,
            fecha_creacion=externo.get("fecha_creacion", ""),
            fecha_actualizacion=externo.get("fecha_actualizacion", ""),
        )

    def dto_a_externo(self, dto: AsociacionDTO) -> dict:
        return {
            "id": str(dto.id),
            "id_marca": str(dto.id_marca),
            "id_socio": str(dto.id_socio),
            "tipo": str(dto.tipo),  # 👈 aseguramos string
            "descripcion": dto.descripcion,
            "vigencia": {
                "fecha_inicio": str(dto.vigencia.fecha_inicio) if dto.vigencia else None,
                "fecha_fin": str(dto.vigencia.fecha_fin) if dto.vigencia else None,
            },
            "fecha_creacion": str(dto.fecha_creacion) if dto.fecha_creacion else None,
            "fecha_actualizacion": str(dto.fecha_actualizacion) if dto.fecha_actualizacion else None,
        }


class MapeadorAsociacion(RepMap):
    """Convierte Entidad de dominio ↔ DTO de aplicación"""

    _FORMATO_FECHA = "%Y-%m-%dT%H:%M:%SZ"

    def obtener_tipo(self) -> type:
        return AsociacionEstrategica.__class__

    def entidad_a_dto(self, entidad: AsociacionEstrategica) -> AsociacionDTO:
        vigencia_dto = VigenciaDTO(
            fecha_inicio=entidad.vigencia.fecha_inicio.strftime(self._FORMATO_FECHA),
            fecha_fin=entidad.vigencia.fecha_fin.strftime(self._FORMATO_FECHA),
        )

        return AsociacionDTO(
            id=str(entidad.id),
            id_marca=str(entidad.id_marca),
            id_socio=str(entidad.id_socio),
            tipo=entidad.tipo.value,
            descripcion=entidad.descripcion,
            vigencia=vigencia_dto,
            fecha_creacion=entidad.fecha_creacion.strftime(self._FORMATO_FECHA),
            fecha_actualizacion=entidad.fecha_actualizacion.strftime(self._FORMATO_FECHA),
        )

    def dto_a_entidad(self, dto: AsociacionDTO) -> AsociacionEstrategica:

        def _parse_fecha(fecha_str, fin=False):
            if len(fecha_str) == 10:
                fecha_str += "T23:59:59" if fin else "T00:00:00"
            return datetime.fromisoformat(fecha_str).replace(tzinfo=timezone.utc)

        fecha_inicio = _parse_fecha(dto.vigencia.fecha_inicio)
        fecha_fin = _parse_fecha(dto.vigencia.fecha_fin, fin=True)

        vigencia = PeriodoVigencia(fecha_inicio, fecha_fin)

        asociacion = AsociacionEstrategica(
            id_marca=dto.id_marca,
            id_socio=dto.id_socio,
            tipo=TipoAsociacion(dto.tipo),
            descripcion=dto.descripcion,
            vigencia=vigencia,
        )

        return asociacion
