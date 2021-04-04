import kivy
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.widget import Widget
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.slider import Slider 
from kivy_garden.graph import Graph, MeshLinePlot
from kivy.clock import Clock
from kivy.properties import ObjectProperty
import numpy as np 
import time
import serialMPU 
import csv
from io import TextIOWrapper
import os

class Inicio(Widget):

    
    def __init__(self, **kwargs):
           
        # Configuracion de Elementos relacionados con la comunicación Serie
        self.sensitivity = 2048 # conversion digital a G
        self.gravedad1 = 0 #constante para restar
        self.gravedad2 = 0 #constante para restar
        self.sampleRate = 500 # SampleRate de Arduino
       
        # Variables lógicas usadas 
        self.status = 0
        self.cuentaFFT = 0
        self.conectado = False
        self.graficosAmplitudDinamica = np.zeros(100)
        self.textosGraficosAmplitudDinamica = []
        # Armado de app Widget con vinculo con archivo de estilo cistas.kv
        # Acomodar
        self.t_max = 15 # Tiempo en segundos que se muestran 
        self.muestras_plot = self.t_max * self.sampleRate

        self.medicioncompleta1 = []
        self.medicioncompleta2 = []

        graph_ac1 = ObjectProperty(None)
        graph_ac2 = ObjectProperty(None)
        boton_on_libre = ObjectProperty(None)
        resetear = ObjectProperty(None)
        exportar = ObjectProperty(None)
        corregir = ObjectProperty(None)
        boton_conectar = ObjectProperty(None)
        texto_usuario = ObjectProperty(None)
        super().__init__(**kwargs)

        # Graficos
        self.plot_ac1 = MeshLinePlot(color=[0.8, 0.6, 0.9, 1])
        self.plot_ac2 = MeshLinePlot(color=[0.4, 0.6, 0.9, 1])
       
    def comunicacionArduino(self,tipo):
        # Rutina para sincronizar con Arduino, creada por FACUNDO RAMON en Processing y Adaptada a Python
        # Escribiendo una "r" el sistema arranca a transmitir
        # Escribiendo una "s" el sistema se detiene     
        # Escribiend un mensaje formado de "v+numero+_" el sistema incluye "numero" como velocidad del motor
        if tipo == "r":
            self.arduino.serialConnection.write(bytes("r", 'ascii'))
           
        elif tipo == "s":
            self.arduino.serialConnection.write(bytes("s", 'ascii'))



    def conectar(self):
        self.texto_usuario.text = ""
        if not self.conectado:

            # Defino parámetros para el objeto Serial
            portName = '/dev/ttyACM0'
            baudRate = 115200
            dataNumBytes = 2        # number of bytes of 1 data point
            numPlots = 2            # number of plots in 1 graph
            
            self.arduino  = serialMPU.serialPlot(serialPort=portName, serialBaud=baudRate, dataNumBytes= dataNumBytes)   # initializes all required variables
            
            a = str(self.arduino.serialConnection.readline())

            if a[-9:-5] == "_OK_":
               
                self.texto_usuario.text = "Sync OK"
                self.texto_usuario.color = (0.1,1,0.1,1)
                self.boton_on_libre.disabled = False
                self.conectado = True
                self.boton_conectar.text = "Desconectar"
                self.boton_conectar.disabled = True

            else:
               
                self.texto_usuario.text = "Sync ERROR"
                self.texto_usuario.color = (1,0.1,0.1,1)
                self.arduino.serialConnection.close()
            
        else:
            self.conectado = False
            self.boton_conectar.text = "Conectar"
            self.arduino.close()
            self.boton_on_libre.disabled = True

    def pressedLibre(self): 
        i = self.status     
        if i == 1:
            self.status = 0
            # Acomodo botones
            self.boton_on_libre.text ="Medir"
            self.boton_conectar.disabled = False
            
            self.resetear.disabled = True
            self.exportar.disabled = True
            self.corregir.disabled = True
            
            # Detengo
            self.stop()
        else:
            self.status = 1
            # Acomodo botones
            self.boton_on_libre.text ="Detener"
            self.boton_conectar.disabled = True
            
            self.resetear.disabled = False
            self.exportar.disabled = False
            self.corregir.disabled = False
           
            # Inicio
            self.startLibre()      

              
    def startLibre(self):
        #Nombre para guardar como CSV
        self.nombreArchivo =  'medicion-'+str(int(np.random.rand(1)*1000))+'-'+str(int(np.random.rand(1)*1000))+'.csv'
        self.graph_ac1.add_plot(self.plot_ac1)
        self.graph_ac2.add_plot(self.plot_ac2)
        
        
        self.comunicacionArduino("r")
        time.sleep(1)
        # Comienzo a ejecutar tarea en 2do plano
        self.arduino.readSerialStart()
        time.sleep(1)
        Clock.schedule_interval(self.modoLibre, 0.1)
        
   
        
    def stop(self):
        Clock.unschedule(self.modoLibre)
        self.resetearWF()
        self.comunicacionArduino("s")
        

    def resetearWF(self):
        # Vuelvo a cero la variable y ajusto los ejes
        self.gravedad1 = np.mean(np.array(self.arduino.valores))
        self.gravedad2 = np.mean(np.array(self.arduino.valores2))

        self.graph_ac1.xmin = 0
        self.graph_ac1.xmax = self.t_max 
       
        self.graph_ac2.xmin = 0
        self.graph_ac2.xmax = self.t_max 

        self.graph_ac1.add_plot(self.plot_ac1)
        self.graph_ac2.add_plot(self.plot_ac2)

        self.plot_ac1.points = []
        self.plot_ac2.points = []

        self.arduino.clearValores()

  
    def cambiarOrdenBits(self):
        self.arduino.corregir = 1

    def exportCSV(self):


        # Genero nombre de archivo con timestamp
        t = time.localtime()
        t = time.strftime('%Y%b%d-%H%M', t)
        dir_path = os.path.dirname(os.path.realpath(__file__))
        self.nombreArchivo = os.path.join(dir_path,"medicion-" + t + ".csv")

        # Abro el csv con TextIOWrapper para hacerlom multiplataforma
        with open(self.nombreArchivo, 'wb') as csvfile, TextIOWrapper(csvfile, encoding='utf-8', newline='') as wrapper:
            csvwriter = csv.writer(wrapper)

            # Genero vector tiempo para exportar
            tiempo = [i / self.sampleRate for i in range(len(self.arduino.valores))]

            # Escribo
            for i in range(0,len(self.arduino.valores)):
                csvwriter.writerows(zip([tiempo[i]], [self.arduino.valores[i]-self.gravedad1], [self.arduino.valores2[i]-self.gravedad2]))

        print("Valores guardados en: "+ self.nombreArchivo)

    
    def modoLibre(self, dt):


        if len(self.arduino.valores) >= self.muestras_plot:

            self.medicioncompleta1.append(self.arduino.valores)
            self.medicioncompleta2.append(self.arduino.valores2)

            self.arduino.clearValores()

            self.plot_ac1.points = []
            self.plot_ac2.points = []

               
        self.plot_ac1.points = [(i/self.sampleRate, j - self.gravedad1) for i, j in enumerate(self.arduino.valores)]
        self.plot_ac2.points = [(i/self.sampleRate, j - self.gravedad2) for i, j in enumerate(self.arduino.valores2)]       
 

        
class MPU6050ArduinoApp(App):

    def build(self):
        return Inicio()


if __name__ == '__main__':
    MPU6050ArduinoApp().run()