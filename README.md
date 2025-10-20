# Intérprete de Lenguaje de Luchadores

Este proyecto es un intérprete para un lenguaje de programación de dominio específico (DSL) diseñado para definir arquetipos de luchadores y simular combates entre ellos. Ha sido desarrollado en **Python** utilizando la librería **PLY (Python Lex-Yacc)** para el análisis léxico y sintáctico.

El objetivo principal es modelar las características de un juego de peleas, permitiendo crear una biblioteca de personajes con movimientos únicos y luego ejecutar una simulación de combate basada en turnos y condiciones.

## Tecnologías Utilizadas

  * **Python 3.10+**
  * **PLY (Python Lex-Yacc)** para la implementación del parser y el lexer.

Para instalar PLY, ejecuta:

```bash
pip install ply
```

##  Estructura del Proyecto

El código está organizado de manera modular para separar las distintas fases del proceso de interpretación:

```
proyecto_luchadores/
│
├── lexer/
│   └── tokens.py           # Analizador Léxico (Flex) - Define los tokens del lenguaje.
│
├── parser_pkg/
│   ├── gramatica.py        # Clases del AST - Define las estructuras de datos (Luchador, Combo, etc.).
│   ├── interprete.py       # Analizador Sintáctico (Bison) - Construye el árbol de objetos del programa.
│   └── motor_combate.py    # Motor de Simulación - Ejecuta el combate a partir del árbol generado por el parser.
│
├── main/
│   └── main.py             # Punto de Entrada - Lee el archivo de código y ejecuta el intérprete.
│
└── ejemplos/
    └── programa.txt        # Código Fuente - Archivo de ejemplo con la definición de luchadores y la simulación.
```

## Características del Lenguaje

El lenguaje se divide en dos grandes bloques: la **definición de luchadores** y la **simulación del combate**.

### 1\. Definición de Luchadores

Permite crear uno o más luchadores, especificando:

  * **`stats`**: Puntos de vida (`hp`) y energía (`st`).
  * **`acciones`**: Movimientos atómicos como `golpe`, `patada` y `bloqueo`, cada uno con atributos como `daño`, `costo`, `altura`, `forma` y si es `giratoria`.
  * **`combos`**: Secuencias nombradas de acciones que requieren una cantidad específica de energía (`st_req`) para ser ejecutadas.

### 2\. Simulación del Combate

Permite configurar y ejecutar una pelea:

  * **`config`**: Define qué dos luchadores de la biblioteca se enfrentarán, quién inicia el combate y el número máximo de turnos.
  * **`pelea`**: Contiene la lógica de los turnos para cada luchador.
  * **Instrucciones**: Dentro de cada turno, un luchador puede `usar` una acción o combo. También puede tomar decisiones basadas en condiciones `si/sino` simples, comparando su propio estado (`self`) o el del rival (`oponente`).

## Cómo Ejecutar el Proyecto

1.  Asegúrate de tener Python y PLY instalados.
2.  Coloca tu archivo de código fuente (por ejemplo, `programa.txt`) dentro de la carpeta `/ejemplos`.
3.  Abre una terminal y navega hasta la carpeta `/main`.
4.  Ejecuta el siguiente comando:

<!-- end list -->

```bash
python main.py
```

El intérprete leerá el archivo, lo parseará con `parser_pkg/interprete.py` para generar el árbol de objetos y luego delegará la simulación a `parser_pkg/motor_combate.py`. El resultado incluye el detalle turno a turno y el desenlace del combate.

## Ejemplo de Código (`programa.txt`)

```
luchador Ryu {
  stats(hp=100, st=100);
  acciones {
    golpe: puño_fuerte(daño=10, costo=7, altura=media, forma=frontal, giratoria=no);
    patada: patada_baja(daño=6, costo=4, altura=baja, forma=frontal, giratoria=no);
    bloqueo: bloqueo_alto;
  }
  combos {
    Hadouken(st_req=25) { puño_fuerte, puño_fuerte }
  }
}

luchador Ken {
  stats(hp=100, st=100);
  acciones {
    golpe: puño_fuerte(daño=10, costo=7, altura=media, forma=frontal, giratoria=no);
    patada: patada_baja(daño=6, costo=4, altura=baja, forma=frontal, giratoria=no);
    bloqueo: bloqueo_bajo;
  }
  combos {
    Uppercut(st_req=25) { puño_fuerte, patada_baja }
  }
}

simulacion {
  config {
    luchadores: Ryu vs Ken;
    inicia: Ryu;
    turnos_max: 10;
  }
  pelea {
    turno Ryu {
      si (oponente.hp < 50) {
          usa Hadouken;
      } sino {
          usa puño_fuerte;
      }
    }
    turno Ken {
      usa puño_fuerte;
    }
  }
}
```

## Funcionamiento Interno

El proceso de interpretación sigue tres etapas clave:

1.  **Análisis Léxico (`lexer/tokens.py`)**: El código fuente en texto plano se descompone en una secuencia de tokens (palabras clave, identificadores, números, símbolos).
2.  **Análisis Sintáctico (`parser_pkg/interprete.py`)**: El parser verifica que la secuencia de tokens siga las reglas gramaticales definidas. Si la sintaxis es correcta, construye un Árbol de Sintaxis Abstracto (AST) utilizando las clases de `gramatica.py`.
3.  **Ejecución (`parser_pkg/motor_combate.py`)**: La función `ejecutar` recibe el programa ya parseado y simula el combate turno por turno. Evalúa las condiciones, aplica el daño, gestiona la energía (ST) y los puntos de vida (HP) de los luchadores hasta que se cumple una condición de fin de combate.
