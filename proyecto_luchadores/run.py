#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ==============================================================
#  run.py - Script automático para ejecutar archivos
# ==============================================================

import sys
from pathlib import Path

# Configurar rutas
script_dir = Path(__file__).parent
sys.path.insert(0, str(script_dir))

def encontrar_archivos_disponibles():
    """Encuentra todos los archivos .txt disponibles"""
    archivos = []
    
    # Buscar en ejemplos/
    carpeta_ejemplos = script_dir / "ejemplos"
    if carpeta_ejemplos.exists():
        archivos.extend(carpeta_ejemplos.glob("*.txt"))
    
    # Buscar en directorio actual
    archivos.extend(Path.cwd().glob("*.txt"))
    
    # Buscar en directorio del script
    archivos.extend(script_dir.glob("*.txt"))
    
    # Eliminar duplicados manteniendo el orden
    archivos_unicos = []
    nombres_vistos = set()
    for archivo in archivos:
        if archivo.name not in nombres_vistos:
            archivos_unicos.append(archivo)
            nombres_vistos.add(archivo.name)
    
    return archivos_unicos

def seleccionar_archivo():
    """Permite al usuario seleccionar un archivo interactivamente"""
    archivos = encontrar_archivos_disponibles()
    
    if not archivos:
        print("No se encontraron archivos .txt")
        return None
    
    if len(archivos) == 1:
        print(f"Usando único archivo disponible: {archivos[0].name}")
        return archivos[0]
    
    print("Archivos disponibles:")
    for i, archivo in enumerate(archivos, 1):
        print(f"   {i}. {archivo.name} ({archivo.parent.name}/)")
    
    while True:
        try:
            seleccion = input(f"\nSelecciona un archivo (1-{len(archivos)}) [Enter=1]: ").strip()
            
            if seleccion == "":
                return archivos[0]
            
            indice = int(seleccion) - 1
            if 0 <= indice < len(archivos):
                return archivos[indice]
            else:
                print(f"Número inválido. Debe estar entre 1 y {len(archivos)}")
                
        except ValueError:
            print("Por favor ingresa un número válido")
        except KeyboardInterrupt:
            print("\nCancelado por el usuario")
            return None

def ejecutar_archivo(ruta_archivo):
    """Ejecuta un archivo del lenguaje de luchadores"""
    
    # Importar módulos necesarios
    try:
        from parser_pkg.interprete import parsear
        from parser_pkg.motor_combate import ejecutar
    except ImportError as e:
        print(f"Error al importar módulos: {e}")
        return False
    
    # Leer archivo
    try:
        with open(ruta_archivo, 'r', encoding='utf-8') as f:
            codigo = f.read()
    except Exception as e:
        print(f"Error al leer el archivo: {e}")
        return False
    
    # Ejecutar
    try:
        print(f"\nEjecutando: {ruta_archivo.name}")
        print("=" * 50)
        
        programa = parsear(codigo)
        ejecutar(programa)
        
        print("=" * 50)
        print("Ejecución completada")
        return True
        
    except Exception as e:
        print(f"Error en la ejecución: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Función principal"""
    print("EJECUTOR DE LENGUAJE DE LUCHADORES")
    print("=" * 40)
    
    archivo = seleccionar_archivo()
    if archivo is None:
        sys.exit(1)
    
    exito = ejecutar_archivo(archivo)
    if not exito:
        sys.exit(1)

if __name__ == "__main__":
    main()
