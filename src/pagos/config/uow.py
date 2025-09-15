from pagos.seedwork.infraestructura.uow import UnidadTrabajo
from sqlalchemy.orm import Session

class UnidadTrabajoSQLAlchemy(UnidadTrabajo):
    def __init__(self, session: Session):
        self._session = session
        self._batches = []
        self._savepoints = []

    @property
    def batches(self):
        return self._batches

    def savepoints(self):
        return self._savepoints

    def _limpiar_batches(self):
        self._batches = []

    def commit(self):
        for batch in self._batches:
            batch.operacion(*batch.args, **batch.kwargs)
        self._session.commit()
        super().commit()

    def rollback(self, savepoint=None):
        if savepoint:
            self._session.rollback()
        else:
            self._session.rollback()
        super().rollback(savepoint)

    def savepoint(self):
        sp = self._session.begin_nested()
        self._savepoints.append(sp)
        return sp
