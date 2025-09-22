# -*- coding: utf-8 -*-
from dataclasses import dataclass
from asociaciones_estrategicas.seedwork.aplicacion.comandos import Comando
from asociaciones_estrategicas.seedwork.infraestructura.pulsar import publicar_comando

@dataclass
class ComandoCrearEventoTracking(Comando):
    id_correlacion: str
    def publicar(self):
        publicar_comando("eventos.comandos.crear_tracking", {"id_correlacion": self.id_correlacion})

@dataclass
class ComandoRevertirEventoTracking(Comando):
    id_correlacion: str
    def publicar(self):
        publicar_comando("eventos.comandos.revertir_tracking", {"id_correlacion": self.id_correlacion})
