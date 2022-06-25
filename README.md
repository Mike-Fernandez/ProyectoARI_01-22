# ProyectoARI_01-22

Aplicativo para análisis de seguridad y testeo con pruebas de seguridad, su función principal es la conversión de archivos en diferentes formatos y la encriptación de datos sensibles así como su recuperación.

## Integrantes

* Miguel Enrique Fernández Azucena 00145518
* Julio Alfredo Machado Olivo 00039718
* Saul Ernesto Orellana Jiménez 00180718
* Nuria Melissa Rivas Canjura 00041517

## Lenguaje de programación

El proyecto fue desarrolado utilizando la versión 3.8 de Python, versiones posteriores también son soportadas

## Librerías

* Tkinter (para la interfaz gráfica del programa)
* PyJWT (para codificar y decodificar JSON Web Tokens)
* Pandas (para usar la función de manipular archivos CSV)
* Librerías de python nativas "xml" y "json" (para la manipulación de este tipo de archivos)

## Funcionalidades

* Archivos CSV a archivo XML
* Archivos CSV a archivo JSON
* Archivos JSON a archivo CSV
* Archivos XML a archivo CSV
* Ingreso de llave para cifrar y codificar utilizando vigenere
* Cifrado y descrifrado utilizando vigenere para datos sensibles
* Generación de archivos JSON Web Token
* Decodificación de JWT a un archivo JSON
* Cuadro de diálogo para elegir ruta de origen y destino de los archivos manipulados
* Vista previa del archivo origen y el formato de destino
* Posibilidad de elegir un delimitador de opciones existentes

## Guía de uso

* Para usar el software se debe correr el archivo Proyecto.py desde la terminal, una vez ejecutado abrirá una ventana la cual es el menú principal de la aplicación
* Debe ingresar una clave de cifrado para los datos dentro de los archivos
* Debe seleccionar un delimitador para sus archivos de texto, si utiliza un delimitador incorrecto, el programa levantara un error y se detendrá.
* Una vez hecho esto, con los botones de acción puede elegir tareas de conversión de archivos libremente, por ejemplo, convertir un archivo separado por comas (CSV) a un archivo XML
* Al terminar de usar el programa puede cerrarlo con el boton "Salir"
