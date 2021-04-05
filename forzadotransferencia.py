import numpy as np
import matplotlib.pyplot as plt
import os
from scipy.signal import savgol_filter

# Nombre de archivo para leer
archivo = "medicion-2021Apr05-082140.csv"


# Lectura de archivo multiplataforma
dir_path = os.path.dirname(os.path.realpath(__file__))
ruta = os.path.join(dir_path,archivo)
data = np.genfromtxt(ruta, delimiter=",", names=["t", "a1", "a2"])
#


fs = 1000

a1 = data['a1']                 # Aceleraciones acelerómetro 1
a2 = data['a2']                 # Aceleraciones acelerómetro 2


# Modificación largo de  para fft
vent = 0
if len(a1)>len(a2):
    vent = len(a1)
else:
    vent = len(a2)


#plt.plot(a1)
#plt.show()

#plt.plot(a2)
#plt.show()

a1_fft = np.fft.rfft(a1,vent+100)
a1_fft = abs(a1_fft)

a1_fft_dB = 10*np.log10(a1_fft)

a1_fft_dB = savgol_filter(a1_fft_dB, 21, 1)

plt.plot(a1_fft_dB)
plt.show()

a2_fft = np.fft.rfft(a2,vent+100)
a2_fft = abs(a2_fft)

a2_fft_dB = 10*np.log10(a2_fft)

a2_fft_dB = savgol_filter(a2_fft_dB, 21, 1)

plt.plot(a2_fft_dB)
plt.show()


T_dB = a2_fft_dB - a1_fft_dB
T = a2/a1
T = np.fft.rfft(T)
f = np.linspace(0, fs/2, len(T))


plt.plot(T_dB)
#plt.plot(a2_fft,)
#plt.plot(a1_fft)
plt.xlim(35,350)
plt.xlabel("Frecuencia [Hz]")
plt.ylabel("Transmisibilidad [dB]")
plt.grid()
plt.show()