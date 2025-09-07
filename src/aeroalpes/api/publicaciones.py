from aeroalpes.modulos.externo.aplicacion.comandos.crear_publicacion import CrearPublicacion
import aeroalpes.seedwork.presentacion.api as api
import json
from aeroalpes.seedwork.dominio.excepciones import ExcepcionDominio

from flask import request
from flask import Response
from aeroalpes.modulos.externo.aplicacion.mapeadores import MapeadorPublicacionDTOJson
from aeroalpes.seedwork.aplicacion.comandos import ejecutar_commando

bp = api.crear_blueprint('publicaciones', '/publicaciones')


@bp.route('/medio-comando', methods=('POST',))
def crear_medio_marketing_asincrono():
    try:
        medio_dict = request.json

        map_publicacion = MapeadorPublicacionDTOJson()
        publicacion_dto = map_publicacion.externo_a_dto(medio_dict)

        comando = CrearPublicacion(publicacion_dto.fecha_creacion, publicacion_dto.fecha_actualizacion, publicacion_dto.id, publicacion_dto.itinerarios)
        
        # TODO Reemplace es todo código sincrono y use el broker de eventos para propagar este comando de forma asíncrona

        ejecutar_commando(comando)
        
        return Response('{}', status=202, mimetype='application/json')
    except ExcepcionDominio as e:
        return Response(json.dumps(dict(error=str(e))), status=400, mimetype='application/json')



@bp.route('/publicacion-comando', methods=('POST',))
def crear_publicacion_asincrona():
    try:
        publicacion_dict = request.json

        map_publicacion = MapeadorPublicacionDTOJson()
        publicacion_dto = map_publicacion.externo_a_dto(publicacion_dict)

        comando = CrearPublicacion(publicacion_dto.fecha_creacion, publicacion_dto.fecha_actualizacion, publicacion_dto.id, publicacion_dto.itinerarios)
        
        # TODO Reemplace es todo código sincrono y use el broker de eventos para propagar este comando de forma asíncrona

        ejecutar_commando(comando)
        
        return Response('{}', status=202, mimetype='application/json')
    except ExcepcionDominio as e:
        return Response(json.dumps(dict(error=str(e))), status=400, mimetype='application/json')


