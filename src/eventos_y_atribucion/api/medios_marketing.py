from eventos_y_atribucion.modulos.eventos_medios.aplicacion.comandos.crear_medio_marketing import CrearMedioMarketing
from eventos_y_atribucion.modulos.eventos_medios.aplicacion.comandos.crear_publicacion import CrearPublicacion
import eventos_y_atribucion.seedwork.presentacion.api as api
import json
from eventos_y_atribucion.seedwork.dominio.excepciones import ExcepcionDominio

from flask import request
from flask import Response
from eventos_y_atribucion.modulos.eventos_medios.aplicacion.mapeadores import MapeadorMedioMarketingDTOJson, MapeadorPublicacionDTOJson
from eventos_y_atribucion.seedwork.aplicacion.comandos import ejecutar_commando

bp = api.crear_blueprint('medios_marketing', '/medios_marketing')


@bp.route('/medio-comando', methods=('POST',))
def crear_medio_marketing_asincrono():
    try:
        medio_dict = request.json

        map_publicacion = MapeadorMedioMarketingDTOJson()
        publicacion_dto = map_publicacion.externo_a_dto(medio_dict)

        comando = CrearMedioMarketing(publicacion_dto.fecha_creacion, publicacion_dto.fecha_actualizacion, publicacion_dto.id)
        
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

        comando = CrearPublicacion(publicacion_dto.fecha_creacion, publicacion_dto.fecha_actualizacion, publicacion_dto.id, publicacion_dto.id_medio_marketing, tipo_publicacion= publicacion_dto.tipo_publicacion)
        
        # TODO Reemplace es todo código sincrono y use el broker de eventos para propagar este comando de forma asíncrona

        ejecutar_commando(comando)
        
        return Response('{}', status=202, mimetype='application/json')
    except ExcepcionDominio as e:
        return Response(json.dumps(dict(error=str(e))), status=400, mimetype='application/json')
    

