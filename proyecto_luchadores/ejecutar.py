#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ==============================================================
#  ejecutar.py
# ==============================================================
#  SCRIPT PARA EJECUTAR ARCHIVOS DEL PROYECTO LUCHADORES
# --------------------------------------------------------------
#  Este script permite ejecutar archivos de diferentes formas:
#   1. Ejecutar el programa principal con archivo por defecto
#   2. Ejecutar con un archivo específico
#   3. Mostrar ayuda y opciones disponibles
# --------------------------------------------------------------
#  Formas de uso:
#      python ejecutar.py                    # Usa programa.txt por defecto
#      python ejecutar.py archivo.txt        # Usa archivo específico
#      python ejecutar.py -h                 # Muestra ayuda
# ==============================================================

import sys
import argparse
from pathlib import Path

# Asegurar que Python pueda importar módulos desde el proyecto
script_dir = Path(__file__).parent
sys.path.insert(0, str(script_dir))

try:
    from parser_pkg.interprete import parsear
    from parser_pkg.motor_combate import ejecutar
except ImportError as e:
    print("xError: No se pudieron importar los módulos necesarios.")
    print(f"   Detalles: {e}")
    print("   Asegúrate de que estás ejecutando el script desde la carpeta del proyecto.")
    sys.exit(1)

def mostrar_banner():
    """Muestra el banner del intérprete"""
    print("=" * 60)
    print("INTÉRPRETE DE LENGUAJE DE LUCHADORES")
    print("=" * 60)

def buscar_archivo(nombre_archivo):
    """
    Busca un archivo en diferentes ubicaciones del proyecto.
    
    Args:
        nombre_archivo (str): Nombre del archivo a buscar
        
    Returns:
        Path: Ruta absoluta del archivo encontrado o None
    """
    # Ubicaciones donde buscar archivos
    ubicaciones = [
        Path.cwd() / nombre_archivo,                    # Directorio actual
        script_dir / nombre_archivo,                    # Carpeta del script
        script_dir / "ejemplos" / nombre_archivo,       # Carpeta ejemplos
        Path(nombre_archivo)                            # Ruta absoluta
    ]
    
    for ubicacion in ubicaciones:
        if ubicacion.exists() and ubicacion.is_file():
            return ubicacion.resolve()
    
    return None

def leer_archivo(ruta_archivo):
    """
    Lee el contenido de un archivo con manejo de errores.
    
    Args:
        ruta_archivo (Path): Ruta del archivo a leer
        
    Returns:
        str: Contenido del archivo o None si hay error
    """
    try:
        with open(ruta_archivo, 'r', encoding='utf-8') as archivo:
            return archivo.read()
    except FileNotFoundError:
        print(f"Error: No se encontró el archivo '{ruta_archivo}'")
        return None
    except UnicodeDecodeError:
        print(f"Error: No se pudo leer el archivo '{ruta_archivo}' (problema de codificación)")
        return None
    except Exception as e:
        print(f"Error inesperado al leer '{ruta_archivo}': {e}")
        return None

def ejecutar_programa(codigo, nombre_archivo):
    """
    Ejecuta el código del lenguaje de luchadores.
    
    Args:
        codigo (str): Código fuente a ejecutar
        nombre_archivo (str): Nombre del archivo (para mostrar)
    """
    try:
        print(f"Analizando archivo: {nombre_archivo}")
        print("-" * 40)
        
        # Analizar el código fuente
        programa = parsear(codigo)
        
        if programa is None:
            print("Error: No se pudo analizar el código correctamente")
            return False
            
        print("Análisis sintáctico completado exitosamente")
        print("-" * 40)
        
        # Ejecutar la simulación
        print("Iniciando simulación de combate...")
        print("-" * 40)
        ejecutar(programa)
        
        print("-" * 40)
        print("Simulación completada")
        return True
        
    except SyntaxError as e:
        print(f"❌ Error de sintaxis: {e}")
        return False
    except Exception as e:
        print(f"❌ Error en la ejecución: {e}")
        import traceback
        print("📋 Detalles técnicos:")
        traceback.print_exc()
        return False

def main():
    """Función principal del script"""
    # Configurar argumentos de línea de comandos
    parser = argparse.ArgumentParser(
        description='Ejecutor del intérprete de lenguaje de luchadores',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Ejemplos de uso:
  python ejecutar.py                    # Ejecuta programa.txt por defecto
  python ejecutar.py mi_combate.txt     # Ejecuta archivo específico
  python ejecutar.py -l                 # Lista archivos disponibles
  python ejecutar.py -v                 # Modo verbose
        """
    )
    
    parser.add_argument(
        'archivo', 
        nargs='?', 
        default='programa.txt',
        help='Archivo a ejecutar (por defecto: programa.txt)'
    )
    
    parser.add_argument(
        '-l', '--listar',
        action='store_true',
        help='Lista archivos disponibles en la carpeta ejemplos'
    )
    
    parser.add_argument(
        '-v', '--verbose',
        action='store_true',
        help='Muestra información detallada'
    )
    
    args = parser.parse_args()
    
    mostrar_banner()
    
    # Opción para listar archivos
    if args.listar:
        carpeta_ejemplos = script_dir / "ejemplos"
        if carpeta_ejemplos.exists():
            archivos = list(carpeta_ejemplos.glob("*.txt"))
            if archivos:
                print("Archivos disponibles en ejemplos/:")
                for archivo in archivos:
                    print(f"   • {archivo.name}")
            else:
                print("No se encontraron archivos .txt en ejemplos/")
        else:
            print("La carpeta ejemplos/ no existe")
        return
    
    # Buscar el archivo especificado
    ruta_archivo = buscar_archivo(args.archivo)
    
    if ruta_archivo is None:
        print(f" No se encontró el archivo '{args.archivo}'")
        print("\nUbicaciones buscadas:")
        print(f"   • Directorio actual: {Path.cwd()}")
        print(f"   • Carpeta del script: {script_dir}")
        print(f"   • Carpeta ejemplos: {script_dir / 'ejemplos'}")
        print("\nUsa 'python ejecutar.py -l' para ver archivos disponibles")
        sys.exit(1)
    
    if args.verbose:
        print(f"Archivo encontrado en: {ruta_archivo}")
    
    # Leer el archivo
    codigo = leer_archivo(ruta_archivo)
    if codigo is None:
        sys.exit(1)
    
    # Ejecutar el programa
    exito = ejecutar_programa(codigo, ruta_archivo.name)
    
    if not exito:
        sys.exit(1)

if __name__ == "__main__":
    main()
