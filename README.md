
# Proyecto de Construcción de AFN y AFD

Este proyecto implementa un analizador léxico simple utilizando autómatas finitos. A partir de una expresión regular en notación postfix, se construye un Autómata Finito No Determinista (AFN) usando el algoritmo de Thompson, luego se convierte el AFN a un Autómata Finito Determinista (AFD) y finalmente se minimiza el AFD.

## Características del Proyecto

- Conversión de expresiones regulares de notación infix a postfix.
- Construcción de AFN utilizando el algoritmo de Thompson.
- Conversión de AFN a AFD utilizando la construcción de subconjuntos.
- Minimización del AFD.
- Simulación de AFN y AFD para verificar si una cadena pertenece al lenguaje definido por la expresión regular.
- Visualización de los autómatas generados usando Graphviz.

## Requisitos

- Python 3.x
- Las dependencias del proyecto se encuentran en el archivo `requirements.txt`. (Aunque por errores en computador se dejó la dependencia de manera fija en la carpeta raiz de este proyecto).

## Instalación

1. Clona este repositorio:
    ```
    git clone <https://github.com/vgcarlol/Proy1-Teoria-Compu>
    ```
2. Navega al directorio del proyecto:
    ```
    cd <Proy1-Teoria-Compu>
    ```
3. Instala las dependencias:
    ```
    pip install -r requirements.txt
    ```

## Uso

1. Crea un archivo de texto en la carpeta `input/` llamado `expressions.txt`.En la primera línea debe contener una expresión regular y luego se le solicitará al usuario que ingrese una cadena para evaluar
    ```
    (a|b)*abb
    ```
3. Ejecuta el programa principal:

    Ingrese la cadena a probar: #Ingresar cadena

4. Ejecuta el programa principal:
    ```
    python src/main.py
    ```
5. Los resultados se generarán en la carpeta `output/` incluyendo las imágenes de los autómatas y los resultados de las simulaciones.

## Archivos del Proyecto

- `src/`: Carpeta principal con los archivos fuente.
  - `main.py`: Archivo principal que ejecuta el proceso completo.
  - `regex_functions.py`: Lógica de manejo de expresiones regulares (infix a postfix).
  - `utilidades.py`: Clases y funciones auxiliares como Stack y Node.
  - `simulacion.py`: Funciones para simular AFN y AFD con una cadena dada.
  - `afn.py`: Lógica para la construcción del AFN.
  - `afd.py`: Lógica para la construcción y simplificación del AFD
  - `graficar.py`: Funciones para graficar el AFN, AFD y AMI
- `input/`: Carpeta que contiene el archivo de entrada `expressions.txt`.
- `output/`: Carpeta donde se guardan las imágenes generadas de los autómatas.
- `requirements.txt`: Lista de dependencias necesarias para el proyecto.

## Dependencias

El proyecto utiliza `graphviz` para la generación de gráficos de los autómatas. Asegúrate de tenerlo instalado y configurado correctamente.

## Notas

- El símbolo `ε` representa la transición epsilon y debe ser utilizado en las expresiones regulares donde sea necesario.
- Este proyecto se desarrolló como una práctica para aprender sobre autómatas finitos y su uso en el análisis léxico.


## Licencia

Este proyecto está bajo la licencia MIT.


## Desarrolladores:
- Carlos Valladares
- Gabriel Paz