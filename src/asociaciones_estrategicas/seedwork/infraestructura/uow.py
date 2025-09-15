# --- imports de arriba ---
from contextvars import ContextVar
# UoW actual (por thread / task)
_current_uow: ContextVar = ContextVar("_current_uow", default=None)

from abc import ABC, abstractmethod
from enum import Enum

from asociaciones_estrategicas.seedwork.dominio.entidades import AgregacionRaiz
from pydispatch import dispatcher

import pickle
import logging
import traceback
from flask import has_request_context, session


class Lock(Enum):
    OPTIMISTA = 1
    PESIMISTA = 2

class Batch:
    def __init__(self, operacion, lock: Lock, *args, **kwargs):
        self.operacion = operacion
        self.args = args
        self.lock = lock
        self.kwargs = kwargs

class UnidadTrabajo(ABC):

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.rollback()

    def _obtener_eventos_rollback(self, batches=None):
        batches = self.batches if batches is None else batches
        eventos = list()
        for batch in batches:
            for arg in batch.args:
                if isinstance(arg, AgregacionRaiz):
                    eventos += arg.eventos_compensacion
                    break
        return eventos

    def _obtener_eventos(self, batches=None):
        batches = self.batches if batches is None else batches
        eventos = list()
        for batch in batches:
            for arg in batch.args:
                if isinstance(arg, AgregacionRaiz):
                    eventos += arg.eventos
                    break
        return eventos

    @abstractmethod
    def _limpiar_batches(self):
        raise NotImplementedError

    @abstractmethod
    def batches(self) -> list[Batch]:
        raise NotImplementedError

    @abstractmethod
    def savepoints(self) -> list:
        raise NotImplementedError                    

    def commit(self):
        self._publicar_eventos_post_commit()
        self._limpiar_batches()

    @abstractmethod
    def rollback(self, savepoint=None):
        self._limpiar_batches()
    
    @abstractmethod
    def savepoint(self):
        raise NotImplementedError

    def registrar_batch(self, operacion, *args, lock=Lock.PESIMISTA, repositorio_eventos_func=None,**kwargs):
        batch = Batch(operacion, lock, *args, **kwargs)
        self.batches.append(batch)
        self._publicar_eventos_dominio(batch, repositorio_eventos_func)

    def _publicar_eventos_dominio(self, batch, repositorio_eventos_func):
        for evento in self._obtener_eventos(batches=[batch]):
            if repositorio_eventos_func:
                repositorio_eventos_func(evento)
            dispatcher.send(signal=f'{type(evento).__name__}Dominio', evento=evento)

    def _publicar_eventos_post_commit(self):
        try:
            for evento in self._obtener_eventos():
                dispatcher.send(signal=f'{type(evento).__name__}Integracion', evento=evento)
        except:
            logging.error('ERROR: Suscribiendose al tópico de eventos!')
            traceback.print_exc()
            

def is_flask():
    try:
        from flask import session
        return True
    except Exception as e:
        return False

def registrar_unidad_de_trabajo(serialized_obj):
    from asociaciones_estrategicas.config.uow import UnidadTrabajoSQLAlchemy
    from flask import session
    

    session['uow'] = serialized_obj

def flask_uow():
    from flask import session
    from asociaciones_estrategicas.config.uow import UnidadTrabajoSQLAlchemy, UnidadTrabajoPulsar
    if session.get('uow'):
        return session['uow']

    uow_serialized = pickle.dumps(UnidadTrabajoSQLAlchemy())
    if session.get('uow_metodo') == 'pulsar':
        uow_serialized = pickle.dumps(UnidadTrabajoPulsar())
    
    registrar_unidad_de_trabajo(uow_serialized)
    return uow_serialized

def unidad_de_trabajo() -> UnidadTrabajo:
    if has_request_context():
        return pickle.loads(flask_uow())
    else:
        # ↓↓↓ mantener la MISMA UoW en el hilo del consumer
        uow = _current_uow.get()
        if uow is None:
            from asociaciones_estrategicas.config.uow import UnidadTrabajoHibrida
            uow = UnidadTrabajoHibrida()
            _current_uow.set(uow)
        return uow

def guardar_unidad_trabajo(uow: UnidadTrabajo):
    if has_request_context():
        registrar_unidad_de_trabajo(pickle.dumps(uow))
    else:
        # fuera de Flask: guarda en thread-local
        _current_uow.set(uow)

def _clear_nonflask_uow():
    if not has_request_context():
        _current_uow.set(None)        


class UnidadTrabajoPuerto:

    @staticmethod
    def commit():
        uow = unidad_de_trabajo()
        uow.commit()
        guardar_unidad_trabajo(uow)
        _clear_nonflask_uow()

    @staticmethod
    def rollback(savepoint=None):
        uow = unidad_de_trabajo()
        uow.rollback(savepoint=savepoint)
        guardar_unidad_trabajo(uow)
        _clear_nonflask_uow()
        
    @staticmethod
    def savepoint():
        uow = unidad_de_trabajo()
        uow.savepoint()
        guardar_unidad_trabajo(uow)

    @staticmethod
    def dar_savepoints():
        uow = unidad_de_trabajo()
        return uow.savepoints()

    @staticmethod
    def registrar_batch(operacion, *args, lock=Lock.PESIMISTA, **kwargs):
        uow = unidad_de_trabajo()
        uow.registrar_batch(operacion, *args, lock=lock, **kwargs)
        guardar_unidad_trabajo(uow)
