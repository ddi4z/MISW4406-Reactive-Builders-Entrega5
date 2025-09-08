from alpespartners.modulos.eventos_medios.dominio.objetos_valor import Odo, ParametroBusca
from alpespartners.modulos.eventos_medios.dominio.entidades import Itinerario, Proveedor
from alpespartners.modulos.eventos_medios.dominio.repositorios import RepositorioProveedores as rp
from alpespartners.seedwork.dominio.servicios import Servicio
from alpespartners.modulos.eventos_medios.dominio.mixins import FiltradoItinerariosMixin
from alpespartners.modulos.eventos_medios.dominio.reglas import MinimoUnAdulto, RutaValida

class ServicioBusqueda(Servicio, FiltradoItinerariosMixin):

    def buscar_itinerarios(self, odos: list[Odo], parametros: ParametroBusca) -> list[Itinerario]:
        itinerarios: list[Itinerario] = list()
        proveedores:list[Proveedor] = rp.obtener_todos()
        
        self.validar_regla(MinimoUnAdulto(parametros.pasajeros))
        [self.validar_regla(RutaValida(ruta)) for odo in odos for segmento in odo.segmentos for ruta in segmento.legs]

        itinerarios.append([proveedor.obtener_itinerarios(odos, parametros) for proveedor in proveedores])

        return self.filtrar_mejores_itinerarios(itinerarios)