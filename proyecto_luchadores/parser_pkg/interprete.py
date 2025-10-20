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

def p_programa(prog):
    """programa : definiciones bloque_simulacion"""
    prog[0] = Programa(tabla_luchadores, prog[2])

# --------------------------------------------------------------
# BLOQUE: DEFINICIONES DE LUCHADORES
# --------------------------------------------------------------

def p_definiciones(prog):
    """definiciones : definicion definiciones
                    | definicion"""
    pass

def p_definicion(prog):
    """definicion : cabecera cuerpo LLAVE_CIERRA"""
    pass

def p_cabecera(prog):
    """cabecera : LUCHADOR ID LLAVE_ABRE"""
    nombre = prog[2]
    tabla_luchadores[nombre] = Luchador(nombre, 0, 0)

def p_cuerpo(prog):
    """cuerpo : stats bloque_acciones bloque_combos"""
    pass

def p_stats(prog):
    """stats : STATS PAREN_ABRE HP IGUAL NUMERO COMA ST IGUAL NUMERO PAREN_CIERRA PUNTO_Y_COMA"""
    nombre = list(tabla_luchadores.keys())[-1]
    luchador = tabla_luchadores[nombre]
    luchador.hp = luchador.hp_max = prog[5]
    luchador.st = luchador.st_max = prog[9]

# --------------------------------------------------------------
# BLOQUE DE ACCIONES
# --------------------------------------------------------------

def p_bloque_acciones(prog):
    """bloque_acciones : ACCIONES LLAVE_ABRE lista_acciones LLAVE_CIERRA"""
    pass

def p_lista_acciones(prog):
    """lista_acciones : accion lista_acciones
                      | accion"""
    pass

def p_accion(prog):
    """accion : GOLPE DOS_PUNTOS lista_golpes PUNTO_Y_COMA
              | PATADA DOS_PUNTOS lista_golpes PUNTO_Y_COMA
              | BLOQUEO DOS_PUNTOS ID PUNTO_Y_COMA"""
    nombre_luchador = list(tabla_luchadores.keys())[-1]
    luchador = tabla_luchadores[nombre_luchador]

    if prog[1].lower() == "bloqueo":
        accion = AccionAtomica("bloqueo", prog[3])
        luchador.acciones[prog[3]] = accion

def p_lista_golpes(prog):
    """lista_golpes : golpe
                    | golpe COMA lista_golpes"""
    prog[0] = [prog[1]] if len(prog) == 2 else [prog[1]] + prog[3]

def p_golpe(prog):
    """golpe : ID PAREN_ABRE atributos PAREN_CIERRA"""
    nombre_luchador = list(tabla_luchadores.keys())[-1]
    luchador = tabla_luchadores[nombre_luchador]
    atributos = prog[3]

    accion = AccionAtomica(
        tipo="golpe",
        nombre=prog[1],
        danio=atributos.get("danio", 0),
        costo=atributos.get("costo", 0),
        altura=atributos.get("altura"),
        forma=atributos.get("forma"),
        giratoria=(atributos.get("giratoria", "no") == "si")
    )
    luchador.acciones[prog[1]] = accion
    prog[0] = accion

def p_atributos(prog):
    """atributos : atributo
                 | atributo COMA atributos"""
    if len(prog) == 2:
        prog[0] = prog[1]
    else:
        d = {}
        d.update(prog[1])
        d.update(prog[3])
        prog[0] = d

def p_atributo(prog):
    """atributo : DANIO IGUAL NUMERO
                | COSTO IGUAL NUMERO
                | ALTURA IGUAL valor_altura
                | FORMA IGUAL valor_forma
                | GIRATORIA IGUAL valor_giro"""
    clave = prog[1].lower()
    if clave == "daño":
        clave = "danio"
    prog[0] = {clave: prog[3]}

def p_valor_altura(prog):
    """valor_altura : ALTA
                    | MEDIA
                    | BAJA"""
    prog[0] = prog[1].lower()

def p_valor_forma(prog):
    """valor_forma : FRONTAL
                   | LATERAL"""
    prog[0] = prog[1].lower()

def p_valor_giro(prog):
    """valor_giro : SI
                  | NO"""
    prog[0] = prog[1].lower()

# --------------------------------------------------------------
# BLOQUE DE COMBOS
# --------------------------------------------------------------

def p_bloque_combos(prog):
    """bloque_combos : COMBOS LLAVE_ABRE lista_combos LLAVE_CIERRA"""
    pass

def p_lista_combos(prog):
    """lista_combos : combo lista_combos
                    | combo"""
    pass

def p_combo(prog):
    """combo : ID PAREN_ABRE ST_REQ IGUAL NUMERO PAREN_CIERRA LLAVE_ABRE lista_ids LLAVE_CIERRA"""
    nombre_luchador = list(tabla_luchadores.keys())[-1]
    luchador = tabla_luchadores[nombre_luchador]
    combo = Combo(prog[1], prog[5], prog[8])
    luchador.combos[prog[1]] = combo

def p_lista_ids(prog):
    """lista_ids : ID
                 | ID COMA lista_ids"""
    prog[0] = [prog[1]] if len(prog) == 2 else [prog[1]] + prog[3]

# --------------------------------------------------------------
# BLOQUE DE SIMULACIÓN
# --------------------------------------------------------------

def p_bloque_simulacion(prog):
    """bloque_simulacion : SIMULACION LLAVE_ABRE configuracion pelea LLAVE_CIERRA"""
    prog[0] = Simulacion(prog[3], prog[4])

def p_configuracion(prog):
    """configuracion : CONFIG LLAVE_ABRE LUCHADORES DOS_PUNTOS ID VS ID PUNTO_Y_COMA INICIA DOS_PUNTOS ID PUNTO_Y_COMA TURNOS_MAX DOS_PUNTOS NUMERO PUNTO_Y_COMA LLAVE_CIERRA"""
    prog[0] = Configuracion(prog[5], prog[7], prog[11], prog[15])

def p_pelea(prog):
    """pelea : PELEA LLAVE_ABRE lista_turnos LLAVE_CIERRA"""
    prog[0] = prog[3]

def p_lista_turnos(prog):
    """lista_turnos : turno
                    | turno lista_turnos"""
    prog[0] = [prog[1]] if len(prog) == 2 else [prog[1]] + prog[2]

def p_turno(prog):
    """turno : TURNO ID LLAVE_ABRE lista_instrucciones LLAVE_CIERRA"""
    prog[0] = Turno(prog[2], prog[4])

def p_lista_instrucciones(prog):
    """lista_instrucciones : instruccion
                           | instruccion lista_instrucciones"""
    prog[0] = [prog[1]] if len(prog) == 2 else [prog[1]] + prog[2]

def p_instruccion(prog):
    """instruccion : USA ID PUNTO_Y_COMA
                   | SI PAREN_ABRE condicion PAREN_CIERRA LLAVE_ABRE lista_instrucciones LLAVE_CIERRA
                   | SI PAREN_ABRE condicion PAREN_CIERRA LLAVE_ABRE lista_instrucciones LLAVE_CIERRA SINO LLAVE_ABRE lista_instrucciones LLAVE_CIERRA"""
    if len(prog) == 4:
        prog[0] = Usar(prog[2])
    elif len(prog) == 8:
        prog[0] = SiSino(prog[3], prog[6], [])
    else:
        prog[0] = SiSino(prog[3], prog[6], prog[10])

def p_condicion(prog):
    """condicion : sujeto_condicion PUNTO atributo_condicion operador NUMERO"""
    prog[0] = Condicion(prog[1], prog[3], prog[4], prog[5])

def p_sujeto_condicion(prog):
    """sujeto_condicion : SELF
                        | OPONENTE"""
    prog[0] = prog[1].lower()

def p_atributo_condicion(prog):
    """atributo_condicion : HP
                          | ST"""
    prog[0] = prog[1].lower()

def p_operador(prog):
    """operador : MENOR
                | MAYOR
                | MENOR_IGUAL
                | MAYOR_IGUAL
                | IGUAL_IGUAL
                | DISTINTO"""
    prog[0] = prog[1]

# --------------------------------------------------------------
# MANEJO DE ERRORES
# --------------------------------------------------------------

def p_error(prog):
    if prog:
        print(f" Error de sintaxis en '{prog.value}' (línea {prog.lineno})")
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
