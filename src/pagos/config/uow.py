from pagos.seedwork.infraestructura.uow import UnidadTrabajo, Batch
from sqlalchemy.orm import Session

class UnidadTrabajoSQLAlchemy(UnidadTrabajo):
    def __init__(self, session: Session):
        self._session = session
        self._batches: list[Batch] = []
        self._savepoints: list[str] = []

    @property
    def session(self) -> Session:
        return self._session

    @property
    def batches(self) -> list[Batch]:
        return self._batches

    def savepoint(self):
        self._session.begin_nested()
        self._savepoints.append("savepoint")

    def savepoints(self) -> list:
        return self._savepoints

    def rollback(self, savepoint=None):
        self._session.rollback()
        self._limpiar_batches()

    def _limpiar_batches(self):
        self._batches = []

    def commit(self):
        self._session.commit()
        super().commit()
