import os

from flask import Flask, jsonify
from flask_swagger import swagger

# Identifica el directorio base
basedir = os.path.abspath(os.path.dirname(__file__))

def registrar_handlers():
    import pagos.modulos.pagos.aplicacion

def importar_modelos_alchemy():
    import pagos.modulos.pagos.infraestructura.dto
    import pagos.modulos.pagos.infraestructura.dto


def comenzar_consumidor(app):
    import threading
    import pagos.modulos.pagos.infraestructura.consumidores as pagos
    # Suscripción a eventos
    threading.Thread(target=pagos.suscribirse_a_eventos, args=[app]).start()

    # Suscripción a comandos
    threading.Thread(target=pagos.suscribirse_a_comandos_crear, args=[app]).start()
    threading.Thread(target=pagos.suscribirse_a_comandos_revertir, args=[app]).start()

def create_app(configuracion={}):
    # Init la aplicacion de Flask
    app = Flask(__name__, instance_relative_config=True)
    
    app.secret_key = '9d58f999-3ae8-4149-a09f-3a8c2012e399'
    app.config['SESSION_TYPE'] = 'filesystem'
    app.config['TESTING'] = configuracion.get('TESTING')

     # Inicializa la DB
    from pagos.config.db import init_db, database_connection

    app.config['SQLALCHEMY_DATABASE_URI'] = database_connection(configuracion, basedir=basedir)
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    init_db(app)

    from pagos.config.db import db

    importar_modelos_alchemy()
    registrar_handlers()

    with app.app_context():
        db.create_all() #No crea las tablas si ya existen
        if not app.config.get('TESTING'):
            comenzar_consumidor(app)

    # Importa Blueprints
    #from . import vuelos
    from . import pagos 

    # Registro de Blueprints
    app.register_blueprint(pagos.bp)

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

app = create_app()