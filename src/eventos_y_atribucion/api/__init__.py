import os

from flask import Flask, jsonify
from flask_swagger import swagger

# Identifica el directorio base
basedir = os.path.abspath(os.path.dirname(__file__))

def registrar_handlers():
    import eventos_y_atribucion.modulos.eventos_medios.aplicacion

def importar_modelos_alchemy():
    import eventos_y_atribucion.modulos.eventos_medios.infraestructura.dto
    import eventos_y_atribucion.modulos.comision_recompensa.infraestructura.dto


def comenzar_consumidor(app):
    import threading
    import eventos_y_atribucion.modulos.eventos_medios.infraestructura.consumidores as eventos
    # Suscripción a eventos
    threading.Thread(target=eventos.suscribirse_a_eventos, args=[app]).start()

    # Suscripción a comandos
    threading.Thread(target=eventos.suscribirse_a_comandos_crear, args=[app]).start()
    threading.Thread(target=eventos.suscribirse_a_comandos_revertir, args=[app]).start()

def create_app(configuracion={}):
    app = Flask(__name__, instance_relative_config=True)

    DB_USER = os.getenv("DB_USER", "postgres")
    DB_PASSWORD = os.getenv("DB_PASSWORD", "pwdadmin")
    DB_HOST = os.getenv("DB_HOST", "localhost")
    DB_PORT = os.getenv("DB_PORT", "5432")
    DB_NAME = os.getenv("DB_NAME", "alpes_partners")


    app.config['SQLALCHEMY_DATABASE_URI'] = (
        f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    )
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    app.secret_key = '9d58f98f-3ae8-4149-a09f-3a8c2012e32c'
    app.config['SESSION_TYPE'] = 'filesystem'
    app.config['TESTING'] = configuracion.get('TESTING')

    # Inicializa la DB
    from eventos_y_atribucion.config.db import init_db, db
    
    init_db(app)
    importar_modelos_alchemy()
    registrar_handlers()

    with app.app_context():
        db.create_all()
        if not app.config.get('TESTING'):
            comenzar_consumidor(app)

    # Importa Blueprints
    from . import medios_marketing
    from . import eventos
    from . import prueba

    app.register_blueprint(medios_marketing.bp)
    app.register_blueprint(eventos.bp)
    app.register_blueprint(prueba.bp)

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
