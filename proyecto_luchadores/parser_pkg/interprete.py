# ==============================================================
#  parser_pkg/interprete.py
# ==============================================================
#  ANALIZADOR SINTÁCTICO + INTÉRPRETE DEL LENGUAJE DE LUCHADORES
# --------------------------------------------------------------
#  Implementa la gramática libre de contexto (GLC) con PLY (yacc)
#  y ejecuta el combate según las reglas del enunciado:
#   - Definición de luchadores, acciones y combos
#   - Bloque de simulación con condiciones y turnos
#   - Lógica de turnos, daño, energía y combos
# ==============================================================

import ply.yacc as yacc
from lexer.tokens import tokens, construir_lexer
from parser_pkg.gramatica import *

# --------------------------------------------------------------
# TABLA DE SÍMBOLOS GLOBAL
# --------------------------------------------------------------
tabla_luchadores = {}

# --------------------------------------------------------------
# REGLAS DE LA GRAMÁTICA
# --------------------------------------------------------------

def p_programa(p):
    """programa : definiciones bloque_simulacion"""
    p[0] = Programa(tabla_luchadores, p[2])

# --------------------------------------------------------------
# BLOQUE: DEFINICIONES DE LUCHADORES
# --------------------------------------------------------------

def p_definiciones(p):
    """definiciones : definicion definiciones
                    | definicion"""
    pass

def p_definicion(p):
    """definicion : cabecera cuerpo LLAVE_CIERRA"""
    pass

def p_cabecera(p):
    """cabecera : LUCHADOR ID LLAVE_ABRE"""
    nombre = p[2]
    tabla_luchadores[nombre] = Luchador(nombre, 0, 0)

def p_cuerpo(p):
    """cuerpo : stats bloque_acciones bloque_combos"""
    pass

def p_stats(p):
    """stats : STATS PAREN_ABRE HP IGUAL NUMERO COMA ST IGUAL NUMERO PAREN_CIERRA PUNTO_Y_COMA"""
    nombre = list(tabla_luchadores.keys())[-1]
    luchador = tabla_luchadores[nombre]
    luchador.hp = luchador.hp_max = p[5]
    luchador.st = luchador.st_max = p[9]

# --------------------------------------------------------------
# BLOQUE DE ACCIONES
# --------------------------------------------------------------

def p_bloque_acciones(p):
    """bloque_acciones : ACCIONES LLAVE_ABRE lista_acciones LLAVE_CIERRA"""
    pass

def p_lista_acciones(p):
    """lista_acciones : accion lista_acciones
                      | accion"""
    pass

def p_accion(p):
    """accion : GOLPE DOS_PUNTOS lista_golpes PUNTO_Y_COMA
              | PATADA DOS_PUNTOS lista_golpes PUNTO_Y_COMA
              | BLOQUEO DOS_PUNTOS ID PUNTO_Y_COMA"""
    nombre_luchador = list(tabla_luchadores.keys())[-1]
    luchador = tabla_luchadores[nombre_luchador]

    if p[1].lower() == "bloqueo":
        accion = AccionAtomica("bloqueo", p[3])
        luchador.acciones[p[3]] = accion

def p_lista_golpes(p):
    """lista_golpes : golpe
                    | golpe COMA lista_golpes"""
    p[0] = [p[1]] if len(p) == 2 else [p[1]] + p[3]

def p_golpe(p):
    """golpe : ID PAREN_ABRE atributos PAREN_CIERRA"""
    nombre_luchador = list(tabla_luchadores.keys())[-1]
    luchador = tabla_luchadores[nombre_luchador]
    atributos = p[3]

    accion = AccionAtomica(
        tipo="golpe",
        nombre=p[1],
        danio=atributos.get("danio", 0),
        costo=atributos.get("costo", 0),
        altura=atributos.get("altura"),
        forma=atributos.get("forma"),
        giratoria=(atributos.get("giratoria", "no") == "si")
    )
    luchador.acciones[p[1]] = accion
    p[0] = accion

def p_atributos(p):
    """atributos : atributo
                 | atributo COMA atributos"""
    if len(p) == 2:
        p[0] = p[1]
    else:
        d = {}
        d.update(p[1])
        d.update(p[3])
        p[0] = d

def p_atributo(p):
    """atributo : DANIO IGUAL NUMERO
                | COSTO IGUAL NUMERO
                | ALTURA IGUAL valor_altura
                | FORMA IGUAL valor_forma
                | GIRATORIA IGUAL valor_giro"""
    clave = p[1].lower()
    if clave == "daño":
        clave = "danio"
    p[0] = {clave: p[3]}

def p_valor_altura(p):
    """valor_altura : ALTA
                    | MEDIA
                    | BAJA"""
    p[0] = p[1].lower()

def p_valor_forma(p):
    """valor_forma : FRONTAL
                   | LATERAL"""
    p[0] = p[1].lower()

def p_valor_giro(p):
    """valor_giro : SI
                  | NO"""
    p[0] = p[1].lower()

# --------------------------------------------------------------
# BLOQUE DE COMBOS
# --------------------------------------------------------------

def p_bloque_combos(p):
    """bloque_combos : COMBOS LLAVE_ABRE lista_combos LLAVE_CIERRA"""
    pass

def p_lista_combos(p):
    """lista_combos : combo lista_combos
                    | combo"""
    pass

def p_combo(p):
    """combo : ID PAREN_ABRE ST_REQ IGUAL NUMERO PAREN_CIERRA LLAVE_ABRE lista_ids LLAVE_CIERRA"""
    nombre_luchador = list(tabla_luchadores.keys())[-1]
    luchador = tabla_luchadores[nombre_luchador]
    combo = Combo(p[1], p[5], p[8])
    luchador.combos[p[1]] = combo

def p_lista_ids(p):
    """lista_ids : ID
                 | ID COMA lista_ids"""
    p[0] = [p[1]] if len(p) == 2 else [p[1]] + p[3]

# --------------------------------------------------------------
# BLOQUE DE SIMULACIÓN
# --------------------------------------------------------------

def p_bloque_simulacion(p):
    """bloque_simulacion : SIMULACION LLAVE_ABRE configuracion pelea LLAVE_CIERRA"""
    p[0] = Simulacion(p[3], p[4])

def p_configuracion(p):
    """configuracion : CONFIG LLAVE_ABRE LUCHADORES DOS_PUNTOS ID VS ID PUNTO_Y_COMA INICIA DOS_PUNTOS ID PUNTO_Y_COMA TURNOS_MAX DOS_PUNTOS NUMERO PUNTO_Y_COMA LLAVE_CIERRA"""
    p[0] = Configuracion(p[5], p[7], p[11], p[15])

def p_pelea(p):
    """pelea : PELEA LLAVE_ABRE lista_turnos LLAVE_CIERRA"""
    p[0] = p[3]

def p_lista_turnos(p):
    """lista_turnos : turno
                    | turno lista_turnos"""
    p[0] = [p[1]] if len(p) == 2 else [p[1]] + p[2]

def p_turno(p):
    """turno : TURNO ID LLAVE_ABRE lista_instrucciones LLAVE_CIERRA"""
    p[0] = Turno(p[2], p[4])

def p_lista_instrucciones(p):
    """lista_instrucciones : instruccion
                           | instruccion lista_instrucciones"""
    p[0] = [p[1]] if len(p) == 2 else [p[1]] + p[2]

def p_instruccion(p):
    """instruccion : USA ID PUNTO_Y_COMA
                   | SI PAREN_ABRE condicion PAREN_CIERRA LLAVE_ABRE lista_instrucciones LLAVE_CIERRA
                   | SI PAREN_ABRE condicion PAREN_CIERRA LLAVE_ABRE lista_instrucciones LLAVE_CIERRA SINO LLAVE_ABRE lista_instrucciones LLAVE_CIERRA"""
    if len(p) == 4:
        p[0] = Usar(p[2])
    elif len(p) == 8:
        p[0] = SiSino(p[3], p[6], [])
    else:
        p[0] = SiSino(p[3], p[6], p[10])

def p_condicion(p):
    """condicion : sujeto_condicion PUNTO atributo_condicion operador NUMERO"""
    p[0] = Condicion(p[1], p[3], p[4], p[5])

def p_sujeto_condicion(p):
    """sujeto_condicion : SELF
                        | OPONENTE"""
    p[0] = p[1].lower()

def p_atributo_condicion(p):
    """atributo_condicion : HP
                          | ST"""
    p[0] = p[1].lower()

def p_operador(p):
    """operador : MENOR
                | MAYOR
                | MENOR_IGUAL
                | MAYOR_IGUAL
                | IGUAL_IGUAL
                | DISTINTO"""
    p[0] = p[1]

# --------------------------------------------------------------
# MANEJO DE ERRORES
# --------------------------------------------------------------

def p_error(p):
    if p:
        print(f" Error de sintaxis en '{p.value}' (línea {p.lineno})")
    else:
        print(" Error de sintaxis al final del archivo")

# --------------------------------------------------------------
# CONSTRUCCIÓN DEL PARSER
# --------------------------------------------------------------

def construir_parser():
    lexer = construir_lexer()
    parser = yacc.yacc(start='programa', debug=False)
    return parser

def parsear(texto):
    tabla_luchadores.clear()
    parser = construir_parser()
    return parser.parse(texto, lexer=construir_lexer())
