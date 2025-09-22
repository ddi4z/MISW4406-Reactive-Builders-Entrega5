import uuid
from pagos.modulos.pagos.aplicacion.comandos.realizar_pago_comision import RealizarPagoComision
from pagos.modulos.pagos.aplicacion.comandos.revertir_pago_comision import RevertirPagoComision
from pagos.modulos.pagos.aplicacion.servicios import ServicioPago
from pagos.seedwork.infraestructura.uow import unidad_de_trabajo
import pagos.seedwork.presentacion.api as api
import json
from pagos.seedwork.dominio.excepciones import ExcepcionDominio

from flask import request, session, Response
from pagos.modulos.pagos.aplicacion.mapeadores import MapeadorPagoDTOJson
from pagos.seedwork.aplicacion.comandos import ejecutar_commando
bp = api.crear_blueprint('pagos', '/pagos')


@bp.route("/ping", methods=('GET',))
def ping():
    return {"pong": 1}
    
    
@bp.route('/crear', methods=('POST',))
def prueba_pagar_comision():
    try:
        session['uow_metodo'] = 'pulsar'
        pago_dict =  request.json

        map_evento = MapeadorPagoDTOJson()
        pago_dto = map_evento.externo_a_dto(pago_dict)
        id_correlacion = pago_dict.get("id_correlacion", "")
        ServicioPago().realizar_pago_comision(pago_dto,id_correlacion)

        
        
        """
       
        comando = RealizarPagoComision(            
            pago_dto.id,
            pago_dto.fecha_creacion,
            pago_dto.fecha_actualizacion,
            pago_dto.id_correlacion,
            pago_dto.id_comision,
            pago_dto.moneda,
            pago_dto.monto,
            pago_dto.metodo_pago,
            pago_dto.estado,
            pago_dto.pasarela
        )
        
        ejecutar_commando(comando)
         """
        
        
        return Response('{}', status=202, mimetype='application/json')
    except ExcepcionDominio as e:
        return Response(json.dumps(dict(error=str(e))), status=400, mimetype='application/json')

@bp.route('/revertir', methods=('POST',))
def prueba_revertir_pago():
    try:
        session['uow_metodo'] = 'pulsar'
        pago_dict = request.json

        id_pago = pago_dict.get("id_pago", str(uuid.uuid4()))  
        id_correlacion = pago_dict.get("id_correlacion", str(uuid.uuid4()))  
        motivo =  pago_dict.get('id_publicacion', '')

        ServicioPago().revertir_pago_comision(id_pago, motivo, id_correlacion)
        #comando = RevertirPagoComision(pago_dto.id)
        #ejecutar_commando(comando)
        
        return Response('{}', status=202, mimetype='application/json')
    except ExcepcionDominio as e:
        return Response(json.dumps(dict(error=str(e))), status=400, mimetype='application/json')