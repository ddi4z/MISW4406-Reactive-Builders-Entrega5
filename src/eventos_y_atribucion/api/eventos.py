import uuid
from eventos_y_atribucion.modulos.eventos_medios.aplicacion.comandos.crear_evento import CrearEvento
from eventos_y_atribucion.modulos.comision_recompensa.aplicacion.comandos.crear_comision import CrearComision
from eventos_y_atribucion.modulos.comision_recompensa.aplicacion.comandos.crear_recompensa import CrearRecompensa
from eventos_y_atribucion.modulos.eventos_medios.aplicacion.queries.obtener_evento import ObtenerEvento
from eventos_y_atribucion.modulos.eventos_medios.aplicacion.servicios import ServicioEvento
from eventos_y_atribucion.seedwork.aplicacion.queries import ejecutar_query
import eventos_y_atribucion.seedwork.presentacion.api as api
import json
from eventos_y_atribucion.seedwork.dominio.excepciones import ExcepcionDominio

from flask import request, session
from flask import Response
from eventos_y_atribucion.modulos.eventos_medios.aplicacion.mapeadores import MapeadorEventoDTOJson
from eventos_y_atribucion.seedwork.aplicacion.comandos import ejecutar_commando
bp = api.crear_blueprint('eventos', '/eventos')



@bp.route('/evento-comando', methods=('POST',))
def crear_evento_asincrono():
    try:
        session['uow_metodo'] = 'pulsar'
        evento_dict = request.json

        map_evento = MapeadorEventoDTOJson()
        evento_dto = map_evento.externo_a_dto(evento_dict)
        id_correlacion = evento_dict.get("id_correlacion", str(uuid.uuid4()))  


        ServicioEvento().crear_evento(evento_dto,id_correlacion)

        #comando = CrearEvento(id_correlacion,evento_dto.fecha_creacion, evento_dto.fecha_actualizacion, evento_dto.id, evento_dto.tipo_evento, evento_dto.id_publicacion)
        #ejecutar_commando(comando)
        
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

