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
            
    def calcular(self,orden_filtro = 21, SampleRate = 1000, plot = False, xlim = []):    

        self.transferencias = {}  
        self.frecuencia = np.fft.rfftfreq(self.fftSize, 1/SampleRate)
        for medicion in range (len (self.leyendas)):
            
            aIN_fft_dB = savgol_filter(10*np.log10(abs(np.fft.rfft(self.aIN[medicion],self.fftSize))),orden_filtro,1)
            aOUT_fft_dB = savgol_filter(10*np.log10(abs(np.fft.rfft(self.aOUT[medicion],self.fftSize))),orden_filtro,1)

            if plot:
                plt.plot(self.frecuencia,aOUT_fft_dB)
                
                if len(xlim)>0:
                    plt.xlim(xlim)
                plt.grid()
                plt.xlabel("Frecuencia [Hz]")
                plt.ylabel("FFT Aceleracion Parlante[dB]")
                plt.show()

                plt.plot(self.frecuencia,aIN_fft_dB)
                if len(xlim)>0:
                    plt.xlim(xlim)
                plt.grid()
                plt.xlabel("Frecuencia [Hz]")
                plt.ylabel("FFT Aceleracion Antivibratorio[dB]")
                plt.show()

            self.transferencias.update({self.leyendas[medicion]:aIN_fft_dB-aOUT_fft_dB})

        
       
    def graficar(self, xlim = []):
        plt.figure()
        for medicion in self.transferencias.keys():
            plt.plot(self.frecuencia,self.transferencias[medicion], label = medicion)
        
        
        plt.xlabel("Frecuencia [Hz]")
        plt.ylabel("Transmisibilidad [dB]")
        
        if len(xlim)>0:
            plt.xlim(xlim)
        plt.legend()
        plt.grid()
        plt.show()

