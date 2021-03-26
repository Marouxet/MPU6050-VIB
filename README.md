# MPU6050-VIB - Acústica y Psicoacústica 1 - Ingeniería de Sonido - Untref
Repositorio para medir vibraciones con arduino y dos acelerómetros  MPU 6050


## Explicación breve del repositorio

* mpu6050x2Arduino.py es el archivo principal, el que se debe ejecutar para correr el programa. Se puede ejecutar desde pycharm (si ya han configurado para que las librerías) o desde la consola(mac) o el anaconda prompt (windows).

Para ejecutarlo desde la consola hacer:

``` 
conda activate acustica1
python mpu6050x2Arduino.py 
```
* mpu6050arduino.kv es un archivo del tipo "kivy", que sirve para crear la interface gráfica. Es llamado desde mpu6050x2Arduino.py 

* serialMPU.py es un archivo que genera la comunicación serie con arduino y paraleliza la parte gráfica. Es llamado internamente desde mpu6050x2Arduino.py 

* subAmortiguadoLibre.py es un script para calcular parámetros del sistema antivibratorios a partir de una medición anterior

* en la carpeta ino hay  una carpeta y dentro de ella un archivo .ino, el mismo es el que debe cargarse al Arduino para que lea aceleración desde los mpu6050.

## Configuración mínima del mpu6050x2Arduino.py

Antes de que puedan leer datos, deben configurar el puerto serie según el sistema operativo. En Windows, los puertos son del tipo 'COM1', "COM2", etc. En Ubuntu son del tipo '/dev/ttyACM0'. En MAC son del tipo '/dev/tty.usbmodem00022331'

### Como detectar el nombre en Windows
* Conectar el arduino
* Abrir el administrador de dispositivos
* Buscar puerto COM y LPT en la lista
* Fijarse el nombre de los puertos activados (debería haber uno solo al menos que tengan otro dispositivo usb conectado)

### Como detectar el nombre en MAC
* Conectar el arduino
* En la consola escribir 
``` 
ls /dev/tty.usb*
``` 
y presionar enter.

Deberían ver únicamente una salida, al menos que haya más dispositivos conectados

![resumen](https://a.pololu-files.com/picture/0J3925.440.png)