from asociaciones_estrategicas.seedwork.infraestructura.vistas import Vista
from asociaciones_estrategicas.modulos.asociaciones.dominio.entidades import AsociacionEstrategica
from asociaciones_estrategicas.config.db import db
from .dto import AsociacionEstrategica as AsociacionDTO
from asociaciones_estrategicas.modulos.asociaciones.dominio.objetos_valor import PeriodoVigencia, TipoAsociacion

class VistaAsociacion(Vista):
    def obtener_por(self, id_asociacion=None, id_marca=None, id_socio=None, tipo=None, **kwargs) -> [AsociacionEstrategica]:
        params = {}

        if id_asociacion:
            params['id'] = str(id_asociacion)
        if id_marca:
            params['id_marca'] = str(id_marca)
        if id_socio:
            params['id_socio'] = str(id_socio)
        if tipo:
            params['tipo'] = str(tipo)

        asociaciones_dto = db.session.query(AsociacionDTO).filter_by(**params)

        # TODO: convertir AsociacionDTO → AsociacionEstrategica (quizás usar MapeadorAsociacion)
        asociaciones = []
        from .mapeadores import MapeadorAsociacionEstrategica
        mapeador = MapeadorAsociacionEstrategica()

        for dto in asociaciones_dto:
            asociaciones.append(mapeador.dto_a_entidad(dto))

        return asociaciones
    
class VistaAnaliticaAsociacion(Vista):
    def obtener_por(self, **kwargs):
        from .dto import AsociacionesAnalitica
        query = db.session.query(AsociacionesAnalitica)
        return query.all()