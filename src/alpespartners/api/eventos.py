from alpespartners.modulos.externo.aplicacion.comandos.crear_evento import CrearEvento
import alpespartners.seedwork.presentacion.api as api
import json
from alpespartners.seedwork.dominio.excepciones import ExcepcionDominio

from flask import request
from flask import Response
from alpespartners.modulos.externo.aplicacion.mapeadores import MapeadorEventoDTOJson
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


