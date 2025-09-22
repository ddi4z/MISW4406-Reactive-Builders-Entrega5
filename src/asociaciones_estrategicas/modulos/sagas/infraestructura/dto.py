
from dataclasses import dataclass
from datetime import datetime
from asociaciones_estrategicas.config.db import db

class SagaLog(db.Model):
    __tablename__ = "saga_log"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_correlacion = db.Column(db.String(64), index=True, nullable=False)
    index = db.Column(db.Integer, nullable=False)
    tipo = db.Column(db.String(64), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self) -> str:
        return f"<SagaLog id={self.id} id_correlacion={self.id_correlacion} paso={self.tipo_paso} index={self.index}>"