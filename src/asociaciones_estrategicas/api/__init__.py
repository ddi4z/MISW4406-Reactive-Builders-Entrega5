import logging
import sys

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)]
)

import os

from flask import Flask, render_template, request, url_for, redirect, jsonify, session
from flask_swagger import swagger

# Identifica el directorio base
basedir = os.path.abspath(os.path.dirname(__file__))

def registrar_handlers():
    import asociaciones_estrategicas.modulos.asociaciones.aplicacion
def importar_modelos_alchemy():
    import asociaciones_estrategicas.modulos.asociaciones.infraestructura.dto

def comenzar_consumidor(app):
    """
    Este es un código de ejemplo. Aunque esto sea funcional puede ser un poco peligroso tener 
    threads corriendo por si solos. Mi sugerencia es en estos casos usar un verdadero manejador
    de procesos y threads como Celery.
    """
    pass #TODO

    import threading
    #import aeroalpes.modulos.vuelos.infraestructura.consumidores as vuelos
    import asociaciones_estrategicas.modulos.asociaciones.infraestructura.consumidores as asociaciones

    # Suscripción a eventos
    threading.Thread(target=asociaciones.suscribirse_a_eventos, args=[app]).start()

    # Suscripción a comandos
    threading.Thread(target=asociaciones.suscribirse_a_comandos_crear, args=[app]).start()
    threading.Thread(target=asociaciones.suscribirse_a_comandos_cancelar, args=[app]).start()

def create_app(configuracion={}):
    # Init la aplicacion de Flask
    app = Flask(__name__, instance_relative_config=True)
    
    app.secret_key = '9d58f999-3ae8-4149-a09f-3a8c2012e399'
    app.config['SESSION_TYPE'] = 'filesystem'
    app.config['TESTING'] = configuracion.get('TESTING')

     # Inicializa la DB
    from asociaciones_estrategicas.config.db import init_db, database_connection

    app.config['SQLALCHEMY_DATABASE_URI'] = database_connection(configuracion, basedir=basedir)
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    init_db(app)

    from asociaciones_estrategicas.config.db import db

    importar_modelos_alchemy()
    registrar_handlers()

    with app.app_context():
        db.create_all() #No crea las tablas si ya existen
        if not app.config.get('TESTING'):
            comenzar_consumidor(app)

    # Importa Blueprints
    #from . import vuelos
    from . import asociaciones 

    # Registro de Blueprints
    app.register_blueprint(asociaciones.bp)

    @app.route("/spec")
    def spec():
        swag = swagger(app)
        swag['info']['version'] = "1.0"
        swag['info']['title'] = "My API"
        return jsonify(swag)

    @app.route("/health")
    def health():
        return {"status": "up"}

    return app
