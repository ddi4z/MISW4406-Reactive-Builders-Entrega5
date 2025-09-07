from alpespartners.modulos.externo.aplicacion.comandos.crear_medio_marketing import CrearMedioMarketing
from alpespartners.modulos.externo.aplicacion.comandos.crear_publicacion import CrearPublicacion
import alpespartners.seedwork.presentacion.api as api
import json
from alpespartners.seedwork.dominio.excepciones import ExcepcionDominio

from flask import request
from flask import Response
from alpespartners.modulos.externo.aplicacion.mapeadores import MapeadorPublicacionDTOJson
from alpespartners.seedwork.aplicacion.comandos import ejecutar_commando

bp = api.crear_blueprint('medios_marketing', '/medios_marketing')


@bp.route('/medio-comando', methods=('POST',))
def crear_medio_marketing_asincrono():
    try:
        medio_dict = request.json

        map_publicacion = MapeadorPublicacionDTOJson()
        publicacion_dto = map_publicacion.externo_a_dto(medio_dict)

        comando = CrearMedioMarketing(publicacion_dto.fecha_creacion, publicacion_dto.fecha_actualizacion, publicacion_dto.id, publicacion_dto.itinerarios)
        
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
    


@bp.route('/plataforma-comando', methods=('POST',))
def crear_plataforma_asincrona():
    try:
        plataforma_dict = request.json

        map_plataforma = MapeadorPublicacionDTOJson()
        plataforma_dto = map_plataforma.externo_a_dto(plataforma_dict)

        comando = CrearPlataforma(plataforma_dto.fecha_creacion, plataforma_dto.fecha_actualizacion, plataforma_dto.id, plataforma_dto.itinerarios)

        # TODO Reemplace es todo código sincrono y use el broker de eventos para propagar este comando de forma asíncrona

        ejecutar_commando(comando)
        
        return Response('{}', status=202, mimetype='application/json')
    except ExcepcionDominio as e:
        return Response(json.dumps(dict(error=str(e))), status=400, mimetype='application/json')
    

