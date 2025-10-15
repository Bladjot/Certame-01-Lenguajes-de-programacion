# ==============================================================
#  parser/interprete.py
# ==============================================================
#  ANALIZADOR SINTÁCTICO + INTÉRPRETE DEL LENGUAJE
# --------------------------------------------------------------
#  Implementa la gramática libre de contexto (GLC) con PLY (yacc)
#  y ejecuta el combate según las reglas del enunciado:
#   - Definición de luchadores, acciones y combos
#   - Bloque de simulación con condiciones y turnos
#   - Lógica de turnos, daño, energía y combos
# ==============================================================

import ply.yacc as yacc
from lexer.tokens import tokens, construir_lexer
from parser.gramatica import *

# --------------------------------------------------------------
# TABLA DE SÍMBOLOS GLOBAL
# --------------------------------------------------------------
# Aquí se almacenan todos los luchadores definidos
tabla_luchadores = {}

# --------------------------------------------------------------
# REGLAS DE LA GRAMÁTICA (EQUIVALENTE A BISON)
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
    """definicion : LUCHADOR ID LLAVE_ABRE cuerpo LLAVE_CIERRA"""
    nombre = p[2]
    tabla_luchadores[nombre] = Luchador(nombre, 0, 0)

def p_cuerpo(p):
    """cuerpo : stats bloque_acciones bloque_combos"""
    pass

def p_stats(p):
    """stats : STATS PAREN_ABRE HP IGUAL NUMERO COMA ST IGUAL NUMERO PAREN_CIERRA PUNTO_Y_COMA"""
    # Actualizar las estadísticas del último luchador creado
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
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = [p[1]] + p[3]

def p_golpe(p):
    """golpe : ID PAREN_ABRE atributos PAREN_CIERRA"""
    nombre_luchador = list(tabla_luchadores.keys())[-1]
    luchador = tabla_luchadores[nombre_luchador]
    atributos = p[3]
    accion = AccionAtomica(
        tipo="golpe",
        nombre=p[1],
        daño=atributos.get("daño", 0),
        costo=atributos.get("costo", 0),
        altura=atributos.get("altura"),
        forma=atributos.get("forma"),
        giratoria=atributos.get("giratoria", False)
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
                | ALTURA IGUAL ID
                | FORMA IGUAL ID
                | GIRATORIA IGUAL ID"""
    clave = p[1].lower()
    valor = p[3]
    p[0] = {clave: valor}

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
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = [p[1]] + p[3]

# --------------------------------------------------------------
# BLOQUE DE SIMULACIÓN
# --------------------------------------------------------------

def p_bloque_simulacion(p):
    """bloque_simulacion : SIMULACION LLAVE_ABRE configuracion pelea LLAVE_CIERRA"""
    p[0] = Simulacion(p[3], p[4])

def p_configuracion(p):
    """configuracion : CONFIG LLAVE_ABRE
                        LUCHADORES DOS_PUNTOS ID VS ID PUNTO_Y_COMA
                        INICIA DOS_PUNTOS ID PUNTO_Y_COMA
                        TURNOS_MAX DOS_PUNTOS NUMERO PUNTO_Y_COMA
                      LLAVE_CIERRA"""
    p[0] = Configuracion(p[5], p[7], p[11], p[15])

def p_pelea(p):
    """pelea : PELEA LLAVE_ABRE lista_turnos LLAVE_CIERRA"""
    p[0] = p[3]

def p_lista_turnos(p):
    """lista_turnos : turno
                    | turno lista_turnos"""
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = [p[1]] + p[2]

def p_turno(p):
    """turno : TURNO ID LLAVE_ABRE lista_instrucciones LLAVE_CIERRA"""
    p[0] = Turno(p[2], p[4])

def p_lista_instrucciones(p):
    """lista_instrucciones : instruccion
                           | instruccion lista_instrucciones"""
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = [p[1]] + p[2]

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
    """condicion : ID PUNTO ID operador NUMERO"""
    p[0] = Condicion(p[1], p[3], p[4], p[5])

def p_operador(p):
    """operador : MENOR
                | MAYOR
                | MENOR_IGUAL
                | MAYOR_IGUAL
                | IGUAL_IGUAL
                | DISTINTO"""
    p[0] = p[1]

def p_error(p):
    if p:
        raise SyntaxError(f"Error de sintaxis cerca de '{p.value}'")
    else:
        raise SyntaxError("Error de sintaxis al final del archivo")

# --------------------------------------------------------------
# EJECUCIÓN DE LA SIMULACIÓN
# --------------------------------------------------------------

def ejecutar(programa):
    sim = programa.simulacion
    l1 = programa.luchadores[sim.config.luch1].clonar()
    l2 = programa.luchadores[sim.config.luch2].clonar()

    turnos = {t.luchador: t for t in sim.turnos}
    orden = [sim.config.inicia, sim.config.luch1 if sim.config.inicia != sim.config.luch1 else sim.config.luch2]

    print(f"\n⚔️  COMBATE: {l1.nombre} vs {l2.nombre}")
    print(f"Turnos máximos: {sim.config.turnos}\n")

    for t in range(sim.config.turnos):
        for quien in orden:
            yo = l1 if quien == l1.nombre else l2
            rival = l2 if yo == l1 else l1

            print(f"➡️  Turno {t+1} de {yo.nombre}:")
            ejecutar_turno(turnos[quien].acciones, yo, rival)

            if l1.hp <= 0 or l2.hp <= 0:
                break

        if l1.hp <= 0 or l2.hp <= 0:
            break

    print("\n🏁 RESULTADO FINAL:")
    print(f"{l1.nombre}: HP={l1.hp}, ST={l1.st}")
    print(f"{l2.nombre}: HP={l2.hp}, ST={l2.st}")
    if l1.hp > l2.hp:
        print(f"🔥 Gana {l1.nombre}")
    elif l2.hp > l1.hp:
        print(f"🔥 Gana {l2.nombre}")
    else:
        print("🤝 Empate")

# --------------------------------------------------------------
# FUNCIONES AUXILIARES DE EJECUCIÓN
# --------------------------------------------------------------

def ejecutar_turno(lista, yo, rival):
    for instr in lista:
        if isinstance(instr, Usar):
            aplicar_accion(instr.nombre, yo, rival)
        elif isinstance(instr, SiSino):
            if instr.condicion.evaluar(yo, rival):
                ejecutar_turno(instr.bloque_si, yo, rival)
            else:
                ejecutar_turno(instr.bloque_sino, yo, rival)

def aplicar_accion(nombre, yo, rival):
    # Si es combo
    if nombre in yo.combos:
        combo = yo.combos[nombre]
        if yo.st >= combo.st_req:
            yo.st -= combo.st_req
            print(f"💥 {yo.nombre} ejecuta combo {nombre}")
            for act in combo.acciones:
                aplicar_accion(act, yo, rival)
        else:
            primero = combo.acciones[0]
            print(f"⚠️ {yo.nombre} no tiene ST suficiente, usa {primero} en su lugar")
            aplicar_accion(primero, yo, rival)
    # Si es acción simple
    elif nombre in yo.acciones:
        a = yo.acciones[nombre]
        if a.tipo == "bloqueo":
            print(f"🛡️ {yo.nombre} usa {nombre} (bloqueo)")
            return
        if yo.st < a.costo:
            print(f"❌ {yo.nombre} no tiene suficiente ST ({yo.st}/{a.costo})")
            return
        yo.st -= a.costo
        rival.hp -= a.daño
        if rival.hp < 0:
            rival.hp = 0
        print(f"🥊 {yo.nombre} usa {nombre} (-{a.daño} HP al rival)")
    else:
        print(f"❌ Acción '{nombre}' no existe para {yo.nombre}")

# --------------------------------------------------------------
# FUNCIÓN DE CONSTRUCCIÓN DEL PARSER
# --------------------------------------------------------------

def construir_parser():
    lexer = construir_lexer()
    parser = yacc.yacc(start='programa')
    return parser

def parsear(texto):
    parser = construir_parser()
    return parser.parse(texto, lexer=construir_lexer())
