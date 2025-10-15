# ==============================================================
#  parser/gramatica.py
# ==============================================================
#  ESTRUCTURAS DE DATOS Y NODOS DE LA GRAMÁTICA
# --------------------------------------------------------------
#  Este archivo define las clases que representan los elementos
#  del lenguaje: luchadores, acciones, combos, condiciones y la
#  simulación del combate.
# --------------------------------------------------------------
#  Es el equivalente a los "árboles de sintaxis" (AST) que crea
#  Bison, pero escrito en Python y con nombres en español.
# ==============================================================

# --------------------------------------------------------------
# CLASE: AccionAtomica
# --------------------------------------------------------------
class AccionAtomica:
    """
    Representa una acción básica del luchador:
    puede ser un golpe, una patada o un bloqueo.
    """
    def __init__(self, tipo, nombre, daño=0, costo=0,
                 altura=None, forma=None, giratoria=False):
        self.tipo = tipo          # "golpe", "patada" o "bloqueo"
        self.nombre = nombre
        self.daño = daño
        self.costo = costo
        self.altura = altura      # alta, media, baja
        self.forma = forma        # frontal o lateral
        self.giratoria = giratoria  # True o False

    def __repr__(self):
        return f"<Acción {self.nombre} ({self.tipo}) daño={self.daño} costo={self.costo}>"

# --------------------------------------------------------------
# CLASE: Combo
# --------------------------------------------------------------
class Combo:
    """
    Representa un conjunto de acciones atómicas.
    """
    def __init__(self, nombre, st_req, acciones):
        self.nombre = nombre
        self.st_req = st_req        # energía requerida
        self.acciones = acciones    # lista de nombres de acciones

    def __repr__(self):
        return f"<Combo {self.nombre} ST_req={self.st_req} acciones={self.acciones}>"

# --------------------------------------------------------------
# CLASE: Luchador
# --------------------------------------------------------------
class Luchador:
    """
    Define a un luchador con sus estadísticas, acciones y combos.
    """
    def __init__(self, nombre, hp, st):
        self.nombre = nombre
        self.hp = hp
        self.st = st
        self.hp_max = hp
        self.st_max = st
        self.acciones = {}   # nombre -> AccionAtomica
        self.combos = {}     # nombre -> Combo

    def clonar(self):
        """
        Devuelve una copia del luchador con las mismas acciones y combos.
        """
        copia = Luchador(self.nombre, self.hp_max, self.st_max)
        copia.acciones = self.acciones
        copia.combos = self.combos
        return copia

    def __repr__(self):
        return f"<Luchador {self.nombre} HP={self.hp} ST={self.st}>"

# --------------------------------------------------------------
# CLASE: Condicion
# --------------------------------------------------------------
class Condicion:
    """
    Representa una condición tipo:
    si (self.hp < 50) { ... } sino { ... }
    """
    def __init__(self, quien, atributo, operador, valor):
        self.quien = quien          # "self" o "oponente"
        self.atributo = atributo    # "hp" o "st"
        self.operador = operador    # <, >, <=, >=, ==, !=
        self.valor = valor          # número

    def evaluar(self, yo, rival):
        """
        Evalúa la condición en tiempo de ejecución.
        """
        if self.quien == 'self':
            actual = yo.hp if self.atributo == 'hp' else yo.st
        else:
            actual = rival.hp if self.atributo == 'hp' else rival.st

        if self.operador == '<':  return actual <  self.valor
        if self.operador == '<=': return actual <= self.valor
        if self.operador == '>':  return actual >  self.valor
        if self.operador == '>=': return actual >= self.valor
        if self.operador == '==': return actual == self.valor
        if self.operador == '!=': return actual != self.valor

    def __repr__(self):
        return f"({self.quien}.{self.atributo} {self.operador} {self.valor})"

# --------------------------------------------------------------
# CLASES: Bloques de simulación
# --------------------------------------------------------------

class Usar:
    """
    Instrucción: usa <acción_o_combo>;
    """
    def __init__(self, nombre):
        self.nombre = nombre

    def __repr__(self):
        return f"<Usar {self.nombre}>"

class SiSino:
    """
    Instrucción condicional: si (...) { ... } sino { ... }
    """
    def __init__(self, condicion, bloque_si, bloque_sino):
        self.condicion = condicion
        self.bloque_si = bloque_si or []
        self.bloque_sino = bloque_sino or []

    def __repr__(self):
        return f"<SiSino {self.condicion}>"

class Turno:
    """
    Define las acciones que ejecuta un luchador en su turno.
    """
    def __init__(self, luchador, acciones):
        self.luchador = luchador
        self.acciones = acciones

    def __repr__(self):
        return f"<Turno {self.luchador} ({len(self.acciones)} acciones)>"

class Configuracion:
    """
    Contiene los parámetros iniciales de la simulación:
    - luchadores involucrados
    - quién inicia
    - cantidad de turnos
    """
    def __init__(self, luch1, luch2, inicia, turnos):
        self.luch1 = luch1
        self.luch2 = luch2
        self.inicia = inicia
        self.turnos = turnos

    def __repr__(self):
        return f"<Config {self.luch1} vs {self.luch2} inicia={self.inicia} turnos={self.turnos}>"

class Simulacion:
    """
    Define la simulación completa:
    configuración inicial + lista de turnos.
    """
    def __init__(self, config, turnos):
        self.config = config
        self.turnos = turnos

    def __repr__(self):
        return f"<Simulacion {self.config}>"

class Programa:
    """
    Programa completo que contiene:
    - Biblioteca de luchadores
    - Simulación de combate
    """
    def __init__(self, luchadores, simulacion):
        self.luchadores = luchadores
        self.simulacion = simulacion

    def __repr__(self):
        return f"<Programa con {len(self.luchadores)} luchadores>"
