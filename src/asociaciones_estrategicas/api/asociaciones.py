import asociaciones_estrategicas.seedwork.presentacion.api as api
import json
from flask import request, session, Response

from asociaciones_estrategicas.seedwork.dominio.excepciones import ExcepcionDominio
from asociaciones_estrategicas.modulos.asociaciones.aplicacion.mapeadores import MapeadorAsociacionDTOJson
from asociaciones_estrategicas.modulos.asociaciones.aplicacion.comandos.crear_asociacion import CrearAsociacion
from asociaciones_estrategicas.modulos.asociaciones.aplicacion.queries.obtener_asociacion import ObtenerAsociacion
from asociaciones_estrategicas.seedwork.aplicacion.comandos import ejecutar_commando
from asociaciones_estrategicas.seedwork.aplicacion.queries import ejecutar_query

bp = api.crear_blueprint('asociaciones', '/asociaciones')


# ==========
# POST: crear asociación
# ==========

@bp.route('', methods=('POST',))
def crear_asociacion_usando_comando():
    try:
        session['uow_metodo'] = 'pulsar'

        asociacion_dict = request.json
        map_asociacion = MapeadorAsociacionDTOJson()
        asociacion_dto = map_asociacion.externo_a_dto(asociacion_dict)

        comando = CrearAsociacion(
            id=asociacion_dto.id,
            id_marca=asociacion_dto.id_marca,
            id_socio=asociacion_dto.id_socio,
            tipo=asociacion_dto.tipo,
            descripcion=asociacion_dto.descripcion,
            fecha_inicio=asociacion_dto.vigencia.fecha_inicio,
            fecha_fin=asociacion_dto.vigencia.fecha_fin,
            fecha_creacion=asociacion_dto.fecha_creacion,
            fecha_actualizacion=asociacion_dto.fecha_actualizacion,
        )

        ejecutar_commando(comando)

        return Response("{}", status=202, mimetype='application/json')
    except ExcepcionDominio as e:
        return Response(
            json.dumps(dict(error=str(e))),
            status=400,
            mimetype='application/json',
        )


# ==========
# GET: obtener asociación
# ==========

@bp.route('', methods=('GET',))
@bp.route('/<id>', methods=('GET',))
def obtener_asociacion_usando_query(id=None):
    if id:
        query_resultado = ejecutar_query(ObtenerAsociacion(id))
        map_asociacion = MapeadorAsociacionDTOJson()

        return map_asociacion.dto_a_externo(query_resultado.resultado)
    else:
        # TODO: aquí podemos implementar una query para listar asociaciones por filtros
        return [{'message': 'GET asociaciones!'}]
