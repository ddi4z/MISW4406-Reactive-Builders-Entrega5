from asociaciones_estrategicas.modulos.asociaciones.aplicacion.queries.obtener_asociacion_analitica import ObtenerAnaliticaAsociaciones
from asociaciones_estrategicas.modulos.asociaciones.aplicacion.queries.obtener_asociacion_lista import ObtenerAsociaciones
from asociaciones_estrategicas.modulos.asociaciones.aplicacion.queries.obtener_asociacion_por_marca import ObtenerAsociacionesPorMarca
from asociaciones_estrategicas.modulos.asociaciones.aplicacion.servicios import ServicioAsociacion
import asociaciones_estrategicas.seedwork.presentacion.api as api
import json
from flask import request, session, Response

from asociaciones_estrategicas.seedwork.dominio.excepciones import ExcepcionDominio
from asociaciones_estrategicas.modulos.asociaciones.aplicacion.mapeadores import MapeadorAsociacionDTOJson
from asociaciones_estrategicas.modulos.asociaciones.aplicacion.comandos.crear_asociacion import CrearAsociacion
from asociaciones_estrategicas.modulos.asociaciones.aplicacion.queries.obtener_asociacion import ObtenerAsociacion
from asociaciones_estrategicas.seedwork.aplicacion.comandos import ejecutar_commando
from asociaciones_estrategicas.seedwork.aplicacion.queries import ejecutar_query
from asociaciones_estrategicas.modulos.asociaciones.aplicacion.mapeadores import MapeadorAnaliticaAsociacionDTOJson

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

        #comando = CrearAsociacion(
        #    id=asociacion_dto.id,
        #    id_marca=asociacion_dto.id_marca,
        #    id_socio=asociacion_dto.id_socio,
        #    tipo=asociacion_dto.tipo,
        #    descripcion=asociacion_dto.descripcion,
        #    fecha_inicio=asociacion_dto.vigencia.fecha_inicio,
        #    fecha_fin=asociacion_dto.vigencia.fecha_fin,
        #    fecha_creacion=asociacion_dto.fecha_creacion,
        #    fecha_actualizacion=asociacion_dto.fecha_actualizacion,
        #)

        # TODO Reemplaze es todo código sincrono y use el broker de eventos para propagar este comando de forma asíncrona
        # Revise la clase Despachador de la capa de infraestructura
        #ejecutar_commando(comando)

        #se pasa la petición al servicio que publica el comando en el broker
        ServicioAsociacion().crear_asociacion(asociacion_dto)

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

@bp.route('/marca/<id_marca>', methods=('GET',))
def obtener_asociaciones_por_marca(id_marca):
    query_resultado = ejecutar_query(ObtenerAsociacionesPorMarca(id_marca))
    map_asociacion = MapeadorAsociacionDTOJson()
    asociaciones_json = []
    for asociacion in query_resultado.resultado:
        asociaciones_json.append(map_asociacion.dto_a_externo(asociacion))
    return asociaciones_json

@bp.route('/lista', methods=('GET',))
def listar_asociaciones():
    id_marca = request.args.get("id_marca")
    id_socio = request.args.get("id_socio")
    tipo = request.args.get("tipo")
    # Si no hay filtros → devuelve un mensaje o lista vacía
    if not any([id_marca, id_socio, tipo]):
        return [{"message": "Use /asociaciones/<id> para buscar por id, o parámetros ?id_marca, ?id_socio, ?tipo"}]
    query_resultado = ejecutar_query(
        ObtenerAsociaciones(id_marca=id_marca, id_socio=id_socio, tipo=tipo)
    )
    map_asociacion = MapeadorAsociacionDTOJson()
    asociaciones_json = []
    for asociacion in query_resultado.resultado:
        asociaciones_json.append(map_asociacion.dto_a_externo(asociacion))
    return asociaciones_json


@bp.route('/analitica', methods=('GET',))
def obtener_analitica_asociaciones():
    query_resultado = ejecutar_query(ObtenerAnaliticaAsociaciones())
    map_analitica = MapeadorAnaliticaAsociacionDTOJson()

    analitica_json = []
    for fila in query_resultado.resultado:
        analitica_json.append(map_analitica.dto_a_externo(fila))

    return analitica_json
