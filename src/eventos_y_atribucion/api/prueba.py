from eventos_y_atribucion.modulos.comision_recompensa.aplicacion.comandos.crear_comision import CrearComision
from eventos_y_atribucion.modulos.comision_recompensa.aplicacion.comandos.crear_recompensa import CrearRecompensa
from eventos_y_atribucion.modulos.comision_recompensa.aplicacion.mapeadores import MapeadorComisionDTOJson, MapeadorRecompensaDTOJson
import eventos_y_atribucion.seedwork.presentacion.api as api
import json
from eventos_y_atribucion.seedwork.dominio.excepciones import ExcepcionDominio

from flask import request
from flask import Response
from eventos_y_atribucion.seedwork.aplicacion.comandos import ejecutar_commando

bp = api.crear_blueprint('prueba', '/prueba')


@bp.route('/comision-comando', methods=('POST',))
def crear_comision_asincrona():
    try:
        comision_dict = request.json

        map_comision = MapeadorComisionDTOJson()
        comision_dto = map_comision.externo_a_dto(comision_dict)

        comando = CrearComision(comision_dto.fecha_creacion, comision_dto.fecha_actualizacion, comision_dto.id, comision_dto.id_evento, comision_dto.valor)
        
        # TODO Reemplace es todo código sincrono y use el broker de eventos para propagar este comando de forma asíncrona

        ejecutar_commando(comando)
        
        return Response('{}', status=202, mimetype='application/json')
    except ExcepcionDominio as e:
        return Response(json.dumps(dict(error=str(e))), status=400, mimetype='application/json')



@bp.route('/recompensa-comando', methods=('POST',))
def crear_recompensa_asincrona():
    try:
        recompensa_dict = request.json

        map_recompensa = MapeadorRecompensaDTOJson()
        recompensa_dto = map_recompensa.externo_a_dto(recompensa_dict)

        comando = CrearRecompensa(recompensa_dto.fecha_creacion, recompensa_dto.fecha_actualizacion, recompensa_dto.id, recompensa_dto.id_evento, descripcion= recompensa_dto.descripcion)
        
        # TODO Reemplace es todo código sincrono y use el broker de eventos para propagar este comando de forma asíncrona

        ejecutar_commando(comando)
        
        return Response('{}', status=202, mimetype='application/json')
    except ExcepcionDominio as e:
        return Response(json.dumps(dict(error=str(e))), status=400, mimetype='application/json')
    

