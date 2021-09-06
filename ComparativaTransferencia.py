import numpy as np
import matplotlib.pyplot as plt
import os
from scipy.signal import savgol_filter


class TransferenciaAceleracion():

    def __init__(self, archivos = [], leyendas = []):
        
        self.t = []
        self.aIN = []
        self.aOUT = []
        self.leyendas = leyendas
        self.fftSize = 0

        # Lectura de archivos multiplataforma y obtención de aceleraciones
        for archivo in archivos:
            dir_path = os.path.dirname(os.path.realpath(__file__))
            ruta = os.path.join(dir_path,archivo)
            data = np.genfromtxt(ruta, delimiter=",", names=["t", "a1", "a2"])

            # Disociar los acelerómetros para saber cuál resta en la ecuación
            amp1 = sum(abs(data['a1']))/len(data['a1'])
            amp2 = sum(abs(data['a2']))/len(data['a2'])

            if amp1<amp2:

               self.aIN.append(data['a1'])
               self.aOUT.append(data['a2'])
               
            else:
               self.aIN.append(data['a2'])
               self.aOUT.append(data['a1'])

            # Definición del largo de la ventana fft
            self.fftSize = max(self.fftSize,len(data['a1']),len(data['a2']))
            
    def calcular(self,orden_filtro = 21, SampleRate = 500):

        global aIN_fft_dB, aOUT_fft_dB

        self.nivelesIN = {}
        self.nivelesOUT = {}
        self.transferencias = {}
        self.frecuencia = np.fft.rfftfreq(self.fftSize, 1/SampleRate)

        for medicion in range (len (self.leyendas)):
            
            aIN_fft_dB = savgol_filter(10*np.log10(abs(np.fft.rfft(self.aIN[medicion],self.fftSize))),orden_filtro,1)
            aOUT_fft_dB = savgol_filter(10*np.log10(abs(np.fft.rfft(self.aOUT[medicion],self.fftSize))),orden_filtro,1)

            self.nivelesIN.update({self.leyendas[medicion]: aIN_fft_dB})
            self.nivelesOUT.update({self.leyendas[medicion]: aOUT_fft_dB})
            self.transferencias.update({self.leyendas[medicion]: aIN_fft_dB-aOUT_fft_dB})
       
    def graficar(self,xlim, plot = True):

        if plot:

            fig, axs = plt.subplots(2, 2)


            for medicion in self.transferencias.keys():
                axs[0,0].plot(self.frecuencia,self.nivelesIN[medicion], 'tab:green')
                axs[0,0].set_title('Acelerómetro 1 [IN]')
                axs[0,0].set(ylabel = 'Amplitud [dB]')
                axs[0,0].grid()

                axs[0,1].plot(self.frecuencia,self.nivelesOUT[medicion],'tab:orange')
                axs[0,1].set_title('Acelerómetro 2 [OUT]')
                axs[0,1].set(ylabel='Amplitud [dB]')
                axs[0,1].grid()

                axs[1,0].plot(self.frecuencia, self.nivelesIN[medicion], 'tab:green')
                axs[1,0].plot(self.frecuencia, self.nivelesOUT[medicion], 'tab:orange')
                axs[1,0].set(xlabel='Frecuencia [Hz]', ylabel='Amplitud [dB]')
                axs[1,0].set_title('Ambos Acelerómetros')
                # axs[1,0].label_outer()
                axs[1,0].grid()

                axs[1,1].plot(self.frecuencia, self.transferencias[medicion])
                axs[1,1].set(xlabel='Frecuencia [Hz]', ylabel='Transmisibilidad [dB]')
                axs[1,1].set_title('Transmisibilidad')
                axs[1,1].grid()



        plt.show()
