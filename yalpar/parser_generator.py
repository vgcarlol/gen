# yalpar/parser_generator.py

import os
from grammar_parser import parse_yalp
from first_follow import compute_first, compute_follow
from lr0_items import items_LR0
from slr_table import build_slr_table

def _dict_para_python(d):
    líneas = []
    líneas.append("{")
    # Ordenamos las claves para reproducibilidad en el output
    for clave in sorted(d.keys()):
        valor = d[clave]
        # clave es una tupla Python, repr(clave) produce "(0, 'ID')"
        # valor puede ser tupla o entero o None; repr(valor) lo imprime correctamente
        lí = f"    {repr(clave)}: {repr(valor)},"
        líneas.append(lí)
    líneas.append("}")
    return "\n".join(líneas)


def generate_parser(yalp_path, salida_py):
    # 1) Parsear la gramática
    gram = parse_yalp(yalp_path)
    tokens = gram['tokens']
    non_terminals = set(gram['non_terminals'])
    productions = gram['productions']
    start_symbol = gram['start_symbol']

    # 2) Calcular FIRST y FOLLOW
    first, _ = compute_first(productions, non_terminals, tokens)
    follow = compute_follow(productions, non_terminals, tokens, start_symbol, first)

    # 3) Construir colección LR(0) y transiciones
    C, transitions, productions_aug, aug_start = items_LR0(productions, non_terminals, start_symbol)

    # 4) Construir tablas ACTION y GOTO
    action, goto = build_slr_table(
        C,
        transitions,
        productions_aug,
        aug_start,
        non_terminals | {aug_start},
        tokens,
        first,
        follow
    )

    # 5) Volcar todo en el archivo Python de salida (sin 'null')
    os.makedirs(os.path.dirname(salida_py), exist_ok=True)
    with open(salida_py, 'w', encoding='utf-8') as f:
        f.write("# AUTO-GENERADO: Parser SLR(1)\n\n")

        # 5.a) Volcar ACTION como diccionario Python
        #     Primero convertimos action (cuya clave es tupla y valor es lista) 
        #     en un dict donde valores sean tuplas Python:
        py_action = {}
        for (i, tok), val in action.items():
            # val es, p.ej., ['shift', 3] o ['reduce', 2] o ['accept', None]
            # lo convertimos a tupla: ('shift', 3), etc.
            py_action[(i, tok)] = tuple(val)

        f.write("ACTION = \\\n")
        f.write(_dict_para_python(py_action))
        f.write("\n\n")

        # 5.b) Volcar GOTO como diccionario Python
        py_goto = {}
        for (i, nt), dest in goto.items():
            py_goto[(i, nt)] = dest

        f.write("GOTO = \\\n")
        f.write(_dict_para_python(py_goto))
        f.write("\n\n")

        # 5.c) Volcar productions_aug (lista de tuplas) directamente
        f.write("productions = [\n")
        for (lhs, rhs) in productions_aug:
            # rhs es lista de strings; lhs es string
            f.write(f"    ({repr(lhs)}, {repr(rhs)}),\n")
        f.write("]\n\n")

        # 5.d) Volcar el símbolo inicial aumentado
        f.write(f"augmented_start = {repr(aug_start)}\n\n")

        # 5.e) Escribir la función parse(tokens) (sin cambios significativos)
        f.write("""
def parse(tokens):
    \"""
    tokens: lista de tuplas (lexema, token), e.g. [('id','ID'), ('+','PLUS'), ..., ('$','$')]
    Simula el parser SLR(1), imprimiendo cada paso (SHIFT, REDUCE, GOTO, ACCEPT).
    Si hay error, lo notifica y devuelve False. Si acepta, devuelve True.
    \"""
    stack_states = [0]
    stack_symbols = []
    i = 0

    while True:
        estado = stack_states[-1]
        if i >= len(tokens):
            print("Error: no hay más tokens, falta '$'")
            return False
        lexema, tok = tokens[i]
        key = (estado, tok)
        if key not in ACTION:
            print(f"Error sintáctico: estado={estado}, token '{tok}' no esperado.")
            return False
        act = ACTION[key]
        if act[0] == 'shift':
            j = act[1]
            stack_states.append(j)
            stack_symbols.append((lexema, tok))
            print(f"SHIFT: estado={estado} --token '{tok}'--> push estado {j}, símbolo ('{lexema}','{tok}')")
            i += 1
        elif act[0] == 'reduce':
            prod_idx = act[1]
            lhs, rhs = productions[prod_idx]
            # Desapilar |rhs| elementos
            for _ in rhs:
                stack_states.pop()
                stack_symbols.pop()
            print(f"REDUCE: usar producción {prod_idx}: {lhs} → {' '.join(rhs)}")
            estado_prev = stack_states[-1]
            goto_key = (estado_prev, lhs)
            if goto_key not in GOTO:
                print(f"Error GOTO: no hay GOTO[{estado_prev}, {lhs}]")
                return False
            new_state = GOTO[goto_key]
            stack_states.append(new_state)
            stack_symbols.append((lhs, 'NT'))
            print(f"GOTO: estado={estado_prev} con no-term '{lhs}' → push estado {new_state}")
        elif act[0] == 'accept':
            print("ACCEPT: cadena sintácticamente correcta.")
            return True
        else:
            print("Acción desconocida en la tabla ACTION.")
            return False
""")
    print(f"✅ Parser generado en: {salida_py}")


if __name__ == '__main__':
    import sys
    if len(sys.argv) != 3:
        print("Uso: python parser_generator.py <ruta_yalp> <ruta_salida_parser.py>")
        print("Ejemplo: python parser_generator.py slr-1.yalp output/parser_slr1.py")
        sys.exit(1)
    yalp_file = sys.argv[1]
    salida = sys.argv[2]
    generate_parser(yalp_file, salida)
