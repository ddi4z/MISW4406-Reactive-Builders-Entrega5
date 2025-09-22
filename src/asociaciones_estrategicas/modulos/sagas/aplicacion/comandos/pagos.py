# -*- coding: utf-8 -*-
from dataclasses import dataclass
from asociaciones_estrategicas.seedwork.aplicacion.comandos import Comando
from asociaciones_estrategicas.seedwork.infraestructura.pulsar import publicar_comando

@dataclass
class RealizarPagoComision(Comando):
    id_correlacion: str
    def publicar(self):
        publicar_comando("pagos.comandos.realizar_comision", {"id_correlacion": self.id_correlacion})

@dataclass
class RevertirPagoComision(Comando):
    id_correlacion: str
    def publicar(self):
        publicar_comando("pagos.comandos.revertir_comision", {"id_correlacion": self.id_correlacion})
