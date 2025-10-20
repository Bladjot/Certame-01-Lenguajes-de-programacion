# ==============================================================
#  parser_pkg/motor_combate.py
# ==============================================================
#  LÓGICA DE EJECUCIÓN DEL COMBATE
# --------------------------------------------------------------
#  Este módulo contiene las funciones encargadas de simular el
#  combate a partir del árbol de objetos generado por el parser.
#  Mantenerlo separado clarifica la responsabilidad de cada parte:
#    - interprete.parsear(...) construye el árbol del programa.
#    - motor_combate.ejecutar(...) interpreta y simula el combate.
# ==============================================================

from parser_pkg.gramatica import Usar, SiSino


def ejecutar(programa):
    """Ejecuta la simulación descrita en el objeto Programa."""
    sim = programa.simulacion
    l1 = programa.luchadores[sim.config.luch1].clonar()
    l2 = programa.luchadores[sim.config.luch2].clonar()

    turnos = {t.luchador: t for t in sim.turnos}
    orden = [
        sim.config.inicia,
        sim.config.luch1 if sim.config.inicia != sim.config.luch1 else sim.config.luch2,
    ]

    print(f"\n  COMBATE: {l1.nombre} vs {l2.nombre}")
    print(f"Turnos máximos: {sim.config.turnos}\n")

    for t in range(sim.config.turnos):
        for quien in orden:
            yo = l1 if quien == l1.nombre else l2
            rival = l2 if yo == l1 else l1

            if quien not in turnos:
                continue

            print(f"  Turno {t + 1} de {yo.nombre}:")
            ejecutar_turno(turnos[quien].acciones, yo, rival)

            if l1.hp <= 0 or l2.hp <= 0:
                break
        if l1.hp <= 0 or l2.hp <= 0:
            break

    print("\n RESULTADO FINAL:")
    print(f"{l1.nombre}: HP={l1.hp}, ST={l1.st}")
    print(f"{l2.nombre}: HP={l2.hp}, ST={l2.st}")
    if l1.hp > l2.hp:
        print(f" Gana {l1.nombre}")
    elif l2.hp > l1.hp:
        print(f" Gana {l2.nombre}")
    else:
        print(" Empate")


def ejecutar_turno(lista, yo, rival):
    """Procesa las instrucciones de un turno para un luchador."""
    for instr in lista:
        if isinstance(instr, Usar):
            aplicar_accion(instr.nombre, yo, rival)
        elif isinstance(instr, SiSino):
            if instr.condicion.evaluar(yo, rival):
                ejecutar_turno(instr.bloque_si, yo, rival)
            else:
                ejecutar_turno(instr.bloque_sino, yo, rival)


def aplicar_accion(nombre, yo, rival):
    """Ejecuta una acción o combo y actualiza los estados."""
    if nombre in yo.combos:
        combo = yo.combos[nombre]
        if yo.st >= combo.st_req:
            yo.st -= combo.st_req
            print(f" {yo.nombre} ejecuta combo {nombre}")
            for act in combo.acciones:
                aplicar_accion(act, yo, rival)
        else:
            primero = combo.acciones[0]
            print(f" {yo.nombre} no tiene ST suficiente, usa {primero} en su lugar")
            aplicar_accion(primero, yo, rival)
    elif nombre in yo.acciones:
        accion = yo.acciones[nombre]
        if accion.tipo == "bloqueo":
            print(f" {yo.nombre} usa {nombre} (bloqueo)")
            return
        if yo.st < accion.costo:
            print(f" {yo.nombre} no tiene suficiente ST ({yo.st}/{accion.costo})")
            return
        yo.st -= accion.costo
        rival.hp -= accion.daño
        rival.hp = max(0, rival.hp)
        print(f" {yo.nombre} usa {nombre} (-{accion.daño} HP al rival)")
    else:
        print(f" Acción '{nombre}' no existe para {yo.nombre}")
