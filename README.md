# Estación Terrena
Código para una estación terrena donde se visualizan distintos datos de sensores.

Tiene como proposito el hacer comprensibles los datos que son transmitidos por una OBC (On board computer) o un CanSat por medio de una cadena de texto en un puerto serial.

![imagen](Imagenes/Interfaz_Blanca.png)

Sigue en desarrollo.

Este proyecto está fuertemente relacionado con
otro proyecto de [ciencia de cohetes y CanSats](https://github.com/el-NASA/POA).

Para poder ejecutarla tienes que:
* Crear un entorno virtual: `virtualenv env`
* Activarlo: `source env/bin/activate`
* Descargar librerias: `pip3 install -r requeriments.txt`
* Correr con: `python3 interfaz.py`

### ¿Que valores espera?
La función `update()` actualiza los gráficos y textos de  la interfaz. Lo primero que hace es obtener una lista con la información que va a actualizar, esta lista se nota como `valor`.

Luego dentro de `update` se ejecutan los métodos *update* específicos de cada elemento que depende esta lista.

Los valores que recibe son:
0. Tiempo de logeo
1. Altura relativa
2. Si se encuentra en caída libre (0 o 1)
3. Temperatura
4. Presión atmosferica
5. Pitch
6. Roll
7. Yaw
8. Acceleracion en X
9. Acceleracion en Y
10. Acceleracion en Z

### ¿Como almacena la información?
Al finalizar la función `update` se ejecuta la función de la clase `bd` llamada `guardar`, esta almacena la anterior lista en el mismo orden añadiendo al final la fecha que se registra en el computador en un archivo **csv**.

Desarrollada por Daniel Alejandro Rodriguez Suarez, líder del semillero de investigación ATL, vinculado al grupo de investigación LIDER de la Universidad Distrital.
