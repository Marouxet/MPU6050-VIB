import ComparativaTransferencia as ct

archivos = ['medicion-2021Apr04-190033.csv',
            'medicion-2021Apr04-190054.csv',
            'medicion-2021Apr05-082140.csv',
            'medicion-2021Apr05-082304.csv']

leyendas = ['Sin peso',
            'Con peso',
            'Sin peso 2',
            'Con un poco más de peso']

archivos = ['medicion-2021Apr04-190033.csv',
            'medicion-2021Apr04-190054.csv']

leyendas = ['Sin peso',
            'Con peso']

Medicion = ct.TransferenciaAceleracion(archivos=archivos, leyendas=leyendas)

Medicion.calcular(plot = True, orden_filtro=41, xlim = [0, 250])

Medicion.graficar(xlim = [0, 300])


