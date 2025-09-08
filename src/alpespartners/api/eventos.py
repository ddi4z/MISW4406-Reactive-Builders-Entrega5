from alpespartners.modulos.eventos_medios.aplicacion.comandos.crear_evento import CrearEvento
from alpespartners.modulos.comision_recompensa.aplicacion.comandos.crear_comision import CrearComision
from alpespartners.modulos.comision_recompensa.aplicacion.comandos.crear_recompensa import CrearRecompensa
from alpespartners.modulos.eventos_medios.aplicacion.queries.obtener_evento import ObtenerEvento
from alpespartners.seedwork.aplicacion.queries import ejecutar_query
import alpespartners.seedwork.presentacion.api as api
import json
from alpespartners.seedwork.dominio.excepciones import ExcepcionDominio

from flask import request
from flask import Response
from alpespartners.modulos.eventos_medios.aplicacion.mapeadores import MapeadorEventoDTOJson
from alpespartners.seedwork.aplicacion.comandos import ejecutar_commando

bp = api.crear_blueprint('eventos', '/eventos')



@bp.route('/evento-comando', methods=('POST',))
def crear_evento_asincrono():
    try:
        evento_dict = request.json

        map_evento = MapeadorEventoDTOJson()
        evento_dto = map_evento.externo_a_dto(evento_dict)

        comando = CrearEvento(evento_dto.fecha_creacion, evento_dto.fecha_actualizacion, evento_dto.id, evento_dto.tipo_evento, evento_dto.id_publicacion)

        # TODO Reemplace es todo código sincrono y use el broker de eventos para propagar este comando de forma asíncrona

        ejecutar_commando(comando)
        
        return Response('{}', status=202, mimetype='application/json')
    except ExcepcionDominio as e:
        return Response(json.dumps(dict(error=str(e))), status=400, mimetype='application/json')


@bp.route('/evento-query', methods=('GET',))
@bp.route('/evento-query/<id>', methods=('GET',))
def dar_evento_usando_query(id=None):
    query_resultado = ejecutar_query(ObtenerEvento(id))
    map_evento = MapeadorEventoDTOJson()
    if id:
        return map_evento.dto_a_externo(query_resultado.resultado)
    return [map_evento.dto_a_externo(evento) for evento in query_resultado.resultado]