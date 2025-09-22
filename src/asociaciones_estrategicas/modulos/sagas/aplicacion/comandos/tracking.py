# -*- coding: utf-8 -*-
from dataclasses import dataclass
from asociaciones_estrategicas.seedwork.aplicacion.comandos import Comando
from asociaciones_estrategicas.seedwork.infraestructura.pulsar import publicar_comando

@dataclass
class ComandoIniciarTracking(Comando):
    id_correlacion: str
    def publicar(self):
        publicar_comando("tracking.comandos.iniciar", {"id_correlacion": self.id_correlacion})

@dataclass
class ComandoCancelarTracking(Comando):
    id_correlacion: str
    def publicar(self):
        publicar_comando("tracking.comandos.cancelar", {"id_correlacion": self.id_correlacion})
