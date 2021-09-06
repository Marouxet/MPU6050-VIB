** Para realizar esta prueba deben estar instaladas las librerías "I2Cdev.h", "MPU6050.h" y "Wire.h" **


Utilizando los códigos Prueba_Acele1.ino y Prueba_Acele2.ino podemos corroborar, de a uno por vez, que los acelerómetros funcionan correctamente, o no.

Para ello debemos abrir uno de los códigos, verificarlo con el TIC que se encuentra a arriba a la izquierda del IDE de Arduino, y luego subirlo, con el 
botón de flecha que se encuentra al lado del TIC.

Luego, debemos abrir el Monitor Serie (la lupita que se encuentra arriba a la derecha). Si todo está bien deberíamos ver cómo se capturan los valores a
medida que pasa el tiempo. Pueden corroborar moviendo el acelerómetro de uan posición horizontal a una vertical, para ver cómo varían los valores en las
columnas. Si no estuviese funcionando, es probable que aparezca un cartel que diga "MPUx FAILED".