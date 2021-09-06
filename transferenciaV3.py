import ComparativaTransferencia as ct

archivos = ['medicion-2021Sep04-173051.csv']

leyendas = ['a']

Medicion = ct.TransferenciaAceleracion(archivos=archivos, leyendas=leyendas)

Medicion.calcular(orden_filtro=41)

Medicion.graficar(xlim=[0,300])


