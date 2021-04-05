import numpy as np
import matplotlib.pyplot as plt
import os

# /// ARCHIVO 1 ///
# Nombre de archivo para leer
# archivo = "medicion-2021Apr04-190033.csv"  # Sin peso
archivo = "medicion-2021Apr05-082140.csv"  # Sin peso


# Lectura de archivo multiplataforma
dir_path = os.path.dirname(os.path.realpath(__file__))
ruta = os.path.join(dir_path,archivo)
data = np.genfromtxt(ruta, delimiter=",", names=["t", "a1", "a2"])
#


fs = 500
a1 = data['a1']                 # Aceleraciones acelerómetro 1
a2 = data['a2']                 # Aceleraciones acelerómetro 2

t = np.arange(0, len(a1)/fs, 1/fs)


# Modificación largo de  para fft
vent = 0
if len(a1)>len(a2):
    vent = len(a1)
else:
    vent = len(a2)

a1_fft = np.fft.rfft(a1,vent+5000)
a1_fft = abs(a1_fft)
a1_fft_dB = 10*np.log10(a1_fft)

a2_fft = np.fft.rfft(a2,vent+5000)
a2_fft = abs(a2_fft)
a2_fft_dB = 10*np.log10(a2_fft)


# Disociar los acelerómetros para saber cuál resta en la ecuación
amp1 = sum(abs(a1))/len(a1)
amp2 = sum(abs(a2))/len(a2)

if amp1>amp2:
    T_dB = a1_fft_dB - a2_fft_dB

else:
     T_dB = a2_fft_dB - a1_fft_dB

# /// Transmisibilidad lineal
# T = a2 / a1
# T = np.fft.rfft(T)
# f = np.linspace(0, fs / 2, len(T))



# /// ARCHIVO 2 : se le agrega el sufijo 2 a todas las variables///
# Nombre de archivo para leer
# archivo2 = "medicion-2021Apr04-190054.csv"  # Con peso
archivo2 = "medicion-2021Apr05-082304.csv"  # Con peso


# Lectura de archivo multiplataforma
dir_path2 = os.path.dirname(os.path.realpath(__file__))
ruta2 = os.path.join(dir_path2,archivo2)
data2 = np.genfromtxt(ruta2, delimiter=",", names=["t2", "a12", "a22"])
#


fs = 500
a12 = data2['a12']                 # Aceleraciones acelerómetro 1
a22 = data2['a22']                 # Aceleraciones acelerómetro 2

t2 = np.arange(0, len(a12)/fs, 1/fs)


# Modificación largo de ventana
vent2 = 0
if len(a12)>len(a22):
    vent2 = len(a12)
else:
    vent2 = len(a22)


a12_fft = np.fft.rfft(a12,vent2+5000)
a12_fft = abs(a12_fft)

a12_fft_dB = 10*np.log10(a12_fft)

a22_fft = np.fft.rfft(a22,vent2+5000)
a22_fft = abs(a22_fft)

a22_fft_dB = 10*np.log10(a22_fft)


# Disociar los acelerómetros para saber cuál resta en la ecuación
amp12 = sum(abs(a12))/len(a12)
amp22 = sum(abs(a22))/len(a22)

if amp12>amp22:
    T_dB2 = a12_fft_dB - a22_fft_dB

else:
     T_dB2 = a22_fft_dB - a12_fft_dB


# /// Transmisibilidad lineal
# T2 = a22/a12
# T2 = np.fft.rfft(T2)
# f2 = np.linspace(0, fs/2, len(T2))


# ///  PLOTEO  ///

plt.plot(T_dB, label='sin peso')
plt.plot(T_dB2, label='con peso')
plt.xlim(15,230)
plt.xlabel("Frecuencia [Hz]")
plt.ylabel("Transmisibilidad [dB]")
plt.legend()
plt.grid()
plt.show()