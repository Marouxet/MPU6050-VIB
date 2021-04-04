 
from threading import Thread
import serial
import time
import collections
import struct
import copy
import os
import numpy as np
  
class serialPlot:
    def __init__(self, serialPort='/dev/ttyACM0', serialBaud=38400, dataNumBytes=2, rango=2, sensibilidad = 2**16):

        self.corregir = 0
        self.port = serialPort
        self.baud = serialBaud
        self.dataNumBytes = dataNumBytes
        
        self.rango = rango
        self.sensibilidad = sensibilidad
        self.rawData = bytearray(dataNumBytes)
        self.rawData2 = bytearray(dataNumBytes)
        self.dataType = None

        if dataNumBytes == 2:
            self.dataType = 'h'     # 2 byte integer
        elif dataNumBytes == 4:
            self.dataType = 'f'     # 4 byte float
        self.data = []
       
        self.isRun = True
        self.isReceiving = False
        self.thread = None
        self.plotTimer = 0
        self.previousTimer = 0
      
        print('Trying to connect to: ' + str(serialPort) + ' at ' + str(serialBaud) + ' BAUD.')
        try:
            #os.system('echo 8323 | sudo -S chmod a+rw /dev/ttyACM0')
            self.serialConnection = serial.Serial(serialPort, serialBaud, timeout=4)
            print('Connected to ' + str(serialPort) + ' at ' + str(serialBaud) + ' BAUD.')
        except:
            print("Failed to connect with " + str(serialPort) + ' at ' + str(serialBaud) + ' BAUD.')
 
    def readSerialStart(self):
        
        if self.thread == None:
            self.valores=[]
            self.valores2=[]
            self.thread = Thread(target=self.backgroundThread)
            self.thread.start()
            # Block till we start receiving values
            while self.isReceiving != True:
                time.sleep(0.1)
        else:
            a = 1
 
    def clearValores(self):
        self.valores = []
        self.valores2 = []

    def backgroundThread(self):    # retrieve data
        time.sleep(1.0)  # give some buffer time for retrieving data
        self.serialConnection.reset_input_buffer()
        
        
        while (self.isRun):
            self.serialConnection.readinto(self.rawData)
            self.serialConnection.readinto(self.rawData2)
            #self.serialConnection.readinto(self.rawData3)
            if self.corregir == 1:
                self.serialConnection.read(1)
                print("Corrigiendo Sincronización")
                self.corregir = 0
            else:
                # Convertir a float desde bytes
                dataFloat = float(struct.unpack('h', self.rawData)[0]*self.rango/self.sensibilidad) # Aceleración en X
                dataFloat2 = float(struct.unpack('h', self.rawData2)[0]*self.rango/self.sensibilidad) # Aceleración en Z
                
                # Agregar vaores a las dos variables que luego lee el otro programa
                self.valores.append(dataFloat)
                self.valores2.append(dataFloat2)
                
                self.isReceiving = True    

 
    def close(self):
        self.isRun = False
        self.thread.join()
        self.serialConnection.close()
        print('Desconectado')

