# ==============================================================
#  main/main.py
# ==============================================================
#  PUNTO DE ENTRADA DEL PROGRAMA
# --------------------------------------------------------------
#  Este archivo se encarga de:
#   1. Leer el archivo de texto (.txt) con la definición del
#      lenguaje (luchadores + simulación).
#   2. Enviarlo al parser para analizar la estructura del código.
#   3. Ejecutar la simulación del combate.
# --------------------------------------------------------------
#  Forma de ejecución:
#      python main.py
# ==============================================================

# 🔧 Asegura que Python pueda importar módulos desde el nivel superior
import sys, os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from parser_pkg.interprete import parsear
from parser_pkg.motor_combate import ejecutar

# --------------------------------------------------------------
# CONFIGURACIÓN DE RUTA DEL ARCHIVO DE ENTRADA
# --------------------------------------------------------------

def obtener_ruta_programa():
    """
    Busca el archivo programa.txt dentro de la carpeta /ejemplos
    relativa a la ubicación actual.
    """
    carpeta_actual = os.path.dirname(__file__)
    ruta = os.path.join(carpeta_actual, "../ejemplos/programa.txt")
    return os.path.abspath(ruta)

# --------------------------------------------------------------
# FUNCIÓN PRINCIPAL
# --------------------------------------------------------------

def main():
    ruta = obtener_ruta_programa()

    print("==============================================")
    print("      INTÉRPRETE DE LENGUAJE DE LUCHADORES")
    print("==============================================")
    print(f"Leyendo archivo: {ruta}\n")

    try:
        with open(ruta, "r", encoding="utf-8") as archivo:
            codigo = archivo.read()
    except FileNotFoundError:
        print(" No se encontró el archivo programa.txt en /ejemplos/")
        return

    try:
        # Analizar el código fuente del lenguaje personalizado
        programa = parsear(codigo)

        # Ejecutar la simulación de combate
        ejecutar(programa)

    except SyntaxError as e:
        print(f"\n Error de sintaxis: {e}")
    except Exception as e:
        print(f"\n Error en la ejecución: {e}")

# --------------------------------------------------------------
# EJECUCIÓN DIRECTA DEL PROGRAMA
# --------------------------------------------------------------

if __name__ == "__main__":
    main()
