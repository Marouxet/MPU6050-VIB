import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import savgol_filter
from matplotlib import gridspec
import os

# Nombre de archivo para leer
archivo = "medicion-2021Apr04-1134.csv"


# Lectura de archivo multiplataforma
dir_path = os.path.dirname(os.path.realpath(__file__))
ruta = os.path.join(dir_path,archivo)
data = np.genfromtxt(ruta, delimiter=",", names=["t", "a1", "a2"])
#

fs = 1000

a1 = data['a1']                 # Aceleraciones acelerómetro 1
a2 = data['a2']                 # Aceleraciones acelerómetro 2

"Funciones locales"

def envolvente(data, fs):
    data = data
    fs = fs

    in_max = int(np.where(data == np.max(data))[0])  # Cortar la data desde el máximo de la respuesta en adelante
    data = data[(in_max):]
    t = np.arange(0, len(data))

    data = savgol_filter(data, 21,
                         1)  # Suavizado de la señal. El segundo parámetro (ventana) podría ser parámetro de elección según el ruido de la medición.
    # el tercer parámetro es el orden del filtro, si es un orden superior a 1 (en esta prueba) toma el ruido como señal.

    #data = data + 0.5  # Esta señal tiene un offset de -0.5 que se compensa acá para centrar la media en 0.

    # plt.plot(t, data)
    # plt.show()

    " Busca los índices donde hay mínimos (b) y máximos (c) locales."

    a = np.diff(np.sign(np.diff(data))).nonzero()[0] + 1  # Máximos y mínimos locales mediante derivada
    b = (np.diff(np.sign(np.diff(data))) > 0).nonzero()[0] + 1  # Mínimos locales (índices)
    c = (np.diff(np.sign(np.diff(data))) < 0).nonzero()[0] + 1  # Máximos locales (índices)

    "Data en los máximos y me quedo con los que quiero"  # Arduo filtrado de máximos y mínimos por errores.

    " MÁXIMOS "  # Máximos que sean positivos.
    data_max = data[c]
    data_max = data_max[data_max > 0]

    t_max = list()  # Índices correspondientes a esos máximos.
    for i in range(len(c)):
        if data[c[i]] > 0:
            t_max.append(c[i])
    t_max = np.array(t_max)

    med_Td = 0  # Estimación bruta del pseudoperíodo por distancia entre máximos.
    for i in range(len(t_max) - 1):
        med_Td = med_Td + (t_max[i + 1] - t_max[i]) / fs

    med_Td = med_Td / (len(t_max) - 1)

    for i in range(1, len(t_max)):  # Queda solo un máximo por pico local. Por ruido de la señal puede haber más de uno.
        if (t_max[i] - t_max[
            i - 1]) < 0.2 * med_Td * fs:  # Se separan dejando solo uno si hay más de uno con una cercanía menor al 20% del
            t_max_prom = (t_max[i - 1] + t_max[
                i]) / 2  # pseudoperíodo estimado. Ese porcentaje también se puede cambiar.
            t_max[i] = t_max_prom
            t_max[i - 1] = -1
        else:
            t_max[i] = t_max[i]
    t_max_del = np.where(t_max == -1)
    t_max = np.delete(t_max, t_max_del[0])

    data_max = data[t_max]

    " MÍNIMOS "  # Ídem anterior pero con mínimos.

    data_min = data[b]
    data_min = data_min[data_min < 0]

    t_min = list()
    for i in range(len(b)):
        if data[b[i]] < 0:
            t_min.append(b[i])
    t_min = np.array(t_min)

    for i in range(1, len(t_min)):
        if (t_min[i] - t_min[i - 1]) < 0.2 * med_Td * fs:
            t_min_prom = (t_min[i - 1] + t_min[i]) / 2
            t_min[i] = t_min_prom
            t_min[i - 1] = -1
        else:
            t_min[i] = t_min[i]
    t_min_del = np.where(t_min == -1)
    t_min = np.delete(t_min, t_min_del[0])

    data_min = data[t_min]

    return data, t, data_max, t_max, data_min, t_min

def calculo(t, data_max, t_max, data_min, t_min):
    " Valor de xi promedio  y pseudoperíodo con todos los máximos relativos "  # El valor de índice de amortiguación y pseudoperíodo promedio considerando máximos/mínimos
    " todos respecto al primer máximo."  # consecutivos entre sí. Se puede hacer con máximos/mínimos todos respecto al primer máximo.

    "CON MÁXIMOS"
    data_max = data_max
    m = 0
    xi_array_max = np.zeros(len(data_max) - 1)
    Td_array_max = np.zeros(len(data_max) - 1)

    for i in range(1, len(data_max)):
        m += 1
        xi_array_max[i - 1] = np.log(data_max[i - 1] / data_max[i]) / (2 * np.pi)
        Td_array_max[i - 1] = (t_max[i] - t_max[i - 1]) / fs

    xi_prom_max = np.mean(xi_array_max)
    xi_std_max = np.std(xi_array_max)
    Td_prom_max = np.mean(Td_array_max)
    Td_std_max = np.std(Td_array_max)

    "CON MÍNIMOS"
    data_min = data_min
    k = 0
    xi_array_min = np.zeros(len(data_min) - 1)
    Td_array_min = np.zeros(len(data_min) - 1)

    for i in range(1, len(data_min)):
        k += 1
        xi_array_min[i - 1] = np.log(data_min[i - 1] / data_min[i]) / (2 * np.pi)
        Td_array_min[i - 1] = (t_min[i] - t_min[i - 1]) / fs

    xi_prom_min = np.mean(xi_array_min)
    xi_std_min = np.std(xi_array_min)
    Td_prom_min = np.mean(Td_array_min)
    Td_std_min = np.std(Td_array_min)

    " Cálculos finales y ecuación sintética para chequear resultados con promedios de máximos y mínimos"

    Td = (Td_prom_max + Td_prom_min) / 2  # Pseudoperíodo [s]
    wd = (2 * np.pi) / Td  # Pseudopulsación [rad/s]
    xi = (xi_prom_max + xi_prom_min) / 2  # Índice de amortiguación
    w0 = wd / np.sqrt(1 - xi ** 2)  # Pulsación natural [rad/s]
    A = np.max(data)  # Amplitud del movimiento

    t_sint = t / fs
    data_sint = A * np.exp(-xi * w0 * t_sint) * np.sin(
        wd * t_sint)  # Respuesta libre sintética subamortiguada con offset

    m = 0.3  # Conociendo el valor de la masa en kg.
    Ra = 2 * xi * m * w0  # Valor de coeficiente de amortiguación promedio de máximos y mínimos en Ns/m
    k = (w0 ** 2) * m  # Rigidez en función de la masa y pulsación natural en N/m

    return m, k, Ra, xi, Td, wd, w0, A, data_sint, t_sint





"Cálculos"

"Acelerómetro 1 y parámetros del sistema"
(data, t, data_max, t_max, data_min, t_min) = envolvente(a1, fs)

(m, k, Ra, xi, Td, wd, w0, A, data_sint, t_sint) = calculo(t, data_max, t_max, data_min, t_min)


"Acelerómetro 2"
(data2, t2, data_max2, t_max2, data_min2, t_min2) = envolvente(a2, fs)      # NO UTILIZADO EN ESTE CASO




"Impresión de resultados en consola"

# print("RESULTADOS PARCIALES :\n")  # Resultados de índice de amortiguación y pseudoperíodo redondeado a 3 decimales con desviación estándar.
#
# print("Xi promediado a partir de máximos:", round(xi_prom_max, 3), ", con desviación:", round(xi_std_max, 3))
# print("Td promediado a partir de máximos:", round(Td_prom_max, 3), "s", ", con desviación:", round(Td_std_max, 3))
# print("Xi promediado a partir de máximos:", round(xi_prom_min, 3), ", con desviación:", round(xi_std_min, 3))
# print("Td promediado a partir de mínimos:", round(Td_prom_min, 3), "s", ", con desviación:", round(Td_std_min, 3))

print("\nRESULTADOS FINALES")
print("Masa:", m, "kg")
print("Índice de amortiguación:", round(xi, 3))
print("Pseudo período", round(Td, 3), "s")
print("Pseudopulsación:", round(wd, 3), "rad/s")
print("Pulsación natural:", round(w0, 3), "rad/s")
print("Frecuencia natural:", round(w0 / (2 * np.pi), 3), "Hz")
print("Coeficiente de amortiguación:", round(Ra, 3), "Ns/m")
print("Rigidez:", round(k, 3), "N/m")



"Plots"

plt.figure(figsize=(9, 6))
gs = gridspec.GridSpec(1, 2, width_ratios=[3, 1])
ax1 = plt.subplot(gs[0])


ax1.plot(t / fs, data_sint, label='Data sintetizada', ls = '--', c = 'silver')
ax1.plot(t / fs, data, label='Respuesta libre', c = 'r')
ax1.plot(t_min / fs, data_min, "o", label='Mínimos')
ax1.plot(t_max / fs, data_max, "o", label='Máximos')
ax1.set_xlabel("Tiempo [s]")
ax1.set_ylabel("ACELERÓMETRO 1 \n \n Amplitud")
ax1.grid()
ax1.legend(loc='upper center', bbox_to_anchor=(0.5, 1.1), ncol=4, fancybox=True, shadow=True)


lim_x = max(t / fs) +1
lim_y = max(data)
paso = max(data) / 5


plt.text(lim_x, lim_y, 'Parámetros: ', fontweight='bold')
plt.text(lim_x, lim_y - paso, r'$m = $' + str(round(m, 3)) + ' ' + r'$ kg$')
plt.text(lim_x, lim_y - 2 * paso, r'$k = $' + str(round(k, 3)) + ' ' + r'$ N/m$')
plt.text(lim_x, lim_y - 3 * paso, r'$w_{0} = $' + str(round(w0, 3)) + ' ' + r'$ rad/s$')
plt.text(lim_x, lim_y - 4 * paso, r'$f_{0} = $' + str(round(w0 / (2 * np.pi), 3)) + ' ' + r'$Hz$')
plt.text(lim_x, lim_y - 5 * paso, r'$T_{0} = $' + str(round((2 * np.pi) / w0, 3)) + ' ' + r'$ s$')
plt.text(lim_x, lim_y - 6 * paso, r'$R_{a} = $' + str(round(Ra, 3)) + ' ' + r'$ Ns/m$')
plt.text(lim_x, lim_y - 7 * paso, r'$\xi = $' + str(round(xi, 3)))
plt.text(lim_x, lim_y - 8 * paso, r'$w_{d} = $' + str(round(wd, 3)) + ' ' + r'$ rad/s$')
plt.text(lim_x, lim_y - 9 * paso, r'$f_{d} = $' + str(round(wd / (2 * np.pi), 3)) + ' ' + r'$Hz$')
plt.text(lim_x, lim_y - 10 * paso, r'$T_{d} = $' + str(round((2 * np.pi) / wd, 3)) + ' ' + r'$ s$')
plt.show()