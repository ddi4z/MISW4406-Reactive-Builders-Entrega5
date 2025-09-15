from sqlalchemy.orm import Session
from eventos_y_atribucion.seedwork.infraestructura.uow import UnidadTrabajo, Batch

class UnidadTrabajoSQLAlchemy(UnidadTrabajo):
    def __init__(self, session: Session):
        self._batches: list[Batch] = []
        self.session = session

    def __enter__(self) -> UnidadTrabajo:
        return super().__enter__()

    def __exit__(self, *args):
        self.rollback()

    def _limpiar_batches(self):
        self._batches = []

    @property
    def savepoints(self) -> list:
        return [self.session.get_nested_transaction()]

    @property
    def batches(self) -> list[Batch]:
        return self._batches

    def commit(self):
        for batch in self.batches:
            lock = batch.lock
            batch.operacion(*batch.args, **batch.kwargs)

        self.session.commit()
        super().commit()

    def rollback(self, savepoint=None):
        if savepoint:
            savepoint.rollback()
        else:
            self.session.rollback()
        
        super().rollback()
    
    def savepoint(self):
        self.session.begin_nested()
