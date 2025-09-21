import logging
from flask_sqlalchemy import SQLAlchemy
from flask import Flask
import os

db = None

DB_USER = os.getenv('DB_USER', default="postgres")
DB_PASSWORD = os.getenv('DB_PASSWORD', default="pwdadmin")
DB_HOST = os.getenv('DB_HOST', default="localhost")
DB_PORT = os.getenv('DB_PORT', default="5432")
DB_NAME = os.getenv('DB_NAME', default="alpes_partners")
DB_SCHEMA = os.getenv('DB_SCHEMA', default="db_asociaciones_estrategicas")

class DatabaseConfigException(Exception):
    def __init__(self, message='Configuration file is Null or malformed'):
        self.message = message
        super().__init__(self.message)


def database_connection(config, basedir=os.path.abspath(os.path.dirname(__file__))) -> str:
    if not isinstance(config, dict):
        raise DatabaseConfigException
    
    if config.get('TESTING', False) is True:
        uri = f'sqlite:///{os.path.join(basedir, "database.db")}'
    else:
        if DB_HOST.startswith("/cloudsql/"):
            # Caso Cloud SQL con Unix socket
            uri = (
                f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@/{DB_NAME}"
                f"?host={DB_HOST}"
            )
        else:
            # Caso conexión TCP normal
            uri = f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

    # Log seguro: no muestra la contraseña
    safe_uri = uri.replace(DB_PASSWORD, "****")
    logging.info(f"Database connection string in use: {safe_uri}")

    return uri



def init_db(app: Flask):
    global db
    if db is None:
        db = SQLAlchemy()
    if 'sqlalchemy' not in app.extensions:
        app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
            "connect_args": {"options": f"-csearch_path={DB_SCHEMA}"}
        }
        db.init_app(app)