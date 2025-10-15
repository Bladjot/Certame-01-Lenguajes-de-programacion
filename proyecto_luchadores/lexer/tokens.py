# -*- coding: utf-8 -*-
# ==============================================================
#  lexer/tokens.py
# ==============================================================
#  ANALIZADOR LÉXICO DEL LENGUAJE DE LUCHADORES
# --------------------------------------------------------------
#  Usa la librería PLY (Python Lex-Yacc) para definir los tokens
#  y expresiones regulares del lenguaje.
# --------------------------------------------------------------
#  El analizador léxico se encarga de:
#   - Detectar palabras reservadas (ej: "luchador", "stats", "usa")
#   - Detectar identificadores (nombres de luchadores y acciones)
#   - Detectar números, símbolos y operadores
#   - Ignorar espacios, saltos de línea y comentarios
# ==============================================================

import ply.lex as lex

# --------------------------------------------------------------
# PALABRAS RESERVADAS
# --------------------------------------------------------------
reservadas = {
    'luchador'   : 'LUCHADOR',
    'stats'      : 'STATS',
    'acciones'   : 'ACCIONES',
    'golpe'      : 'GOLPE',
    'patada'     : 'PATADA',
    'bloqueo'    : 'BLOQUEO',
    'combos'     : 'COMBOS',
    'simulacion' : 'SIMULACION',
    'config'     : 'CONFIG',
    'luchadores' : 'LUCHADORES',
    'inicia'     : 'INICIA',
    'turnos_max' : 'TURNOS_MAX',
    'pelea'      : 'PELEA',
    'turno'      : 'TURNO',
    'si'         : 'SI',
    'sino'       : 'SINO',
    'usa'        : 'USA',

    # Entidades para condiciones
    'self'       : 'SELF',
    'oponente'   : 'OPONENTE',
    'hp'         : 'HP',
    'st'         : 'ST',

    # Atributos y valores de acciones
    'daño'       : 'DANIO',
    'costo'      : 'COSTO',
    'altura'     : 'ALTURA',
    'forma'      : 'FORMA',
    'giratoria'  : 'GIRATORIA',
    'alta'       : 'ALTA',
    'media'      : 'MEDIA',
    'baja'       : 'BAJA',
    'frontal'    : 'FRONTAL',
    'lateral'    : 'LATERAL',
    'no'         : 'NO',

    # Otros
    'st_req'     : 'ST_REQ',
    'vs'         : 'VS'
}

# --------------------------------------------------------------
# LISTA DE TOKENS
# --------------------------------------------------------------
tokens = [
    # Identificadores y números
    'ID', 'NUMERO',

    # Símbolos estructurales
    'LLAVE_ABRE', 'LLAVE_CIERRA',
    'PAREN_ABRE', 'PAREN_CIERRA',
    'COMA', 'PUNTO_Y_COMA', 'DOS_PUNTOS', 'IGUAL', 'PUNTO',

    # Operadores de comparación
    'MENOR', 'MAYOR', 'MENOR_IGUAL', 'MAYOR_IGUAL', 'IGUAL_IGUAL', 'DISTINTO',
] + list(reservadas.values())

# --------------------------------------------------------------
# EXPRESIONES REGULARES PARA TOKENS SIMPLES
# --------------------------------------------------------------
t_LLAVE_ABRE   = r'\{'
t_LLAVE_CIERRA = r'\}'
t_PAREN_ABRE   = r'\('
t_PAREN_CIERRA = r'\)'
t_COMA         = r','
t_PUNTO_Y_COMA = r';'
t_DOS_PUNTOS   = r':'
t_IGUAL        = r'='
t_PUNTO        = r'\.'     # ← necesario para self.hp / oponente.st

# Operadores relacionales
t_MENOR_IGUAL  = r'<='
t_MAYOR_IGUAL  = r'>='
t_MENOR        = r'<'
t_MAYOR        = r'>'
t_IGUAL_IGUAL  = r'=='
t_DISTINTO     = r'!='

# --------------------------------------------------------------
# TOKENS CON ACCIONES (funciones)
# --------------------------------------------------------------
def t_NUMERO(t):
    r'\d+'
    t.value = int(t.value)
    return t

# Fuerza la prioridad de palabras reservadas sobre ID
def t_ID(t):
    r'[A-Za-z_áéíóúÁÉÍÓÚñÑ][A-Za-z0-9_áéíóúÁÉÍÓÚñÑ]*'
    palabra = t.value.lower()
    if palabra == "vs":
        t.type = "VS"
    else:
        t.type = reservadas.get(palabra, 'ID')
    return t


# --------------------------------------------------------------
# REGLAS ESPECIALES
# --------------------------------------------------------------
def t_COMENTARIO(t):
    r'//[^\n]*'
    pass  # Ignorar comentarios

t_ignore = ' \t\r'  # Espacios y tabulaciones

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

def t_error(t):
    print(f"⚠️  Caracter no permitido: '{t.value[0]}' en la línea {t.lexer.lineno}")
    t.lexer.skip(1)

# --------------------------------------------------------------
# CONSTRUCTOR DEL LÉXER
# --------------------------------------------------------------
def construir_lexer(**kwargs):
    """
    Construye y devuelve el analizador léxico.
    """
    return lex.lex(**kwargs)
