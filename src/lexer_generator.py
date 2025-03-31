import os

def generar_lexer_py(afd, token_map, ruta_salida="output/lexer.py"):
    os.makedirs(os.path.dirname(ruta_salida), exist_ok=True)

    with open(ruta_salida, "w", encoding="utf-8") as f:
        f.write("""# AUTO-GENERADO: Analizador léxico basado en AFD

def analizar(texto):
    transitions = {
""")

        for (estado, simbolo), destino in afd.getTransitions().items():
            # Usar repr para ambas partes:
            estado_str = repr(estado)      # p.ej. 'A' o '10'
            simbolo_str = repr(simbolo)    # p.ej. '\\' => "'\\\\'"
            destino_str = repr(destino)    # p.ej. 'B'

            f.write(f"        ({estado_str}, {simbolo_str}): {destino_str},\n")

        f.write("    }\n\n")

        f.write("    accepting = {\n")
        for st, (token_id, token_name) in token_map.items():
            # token_name es un string también
            token_name_str = repr(token_name)
            f.write(f"        {repr(st)}: {token_name_str},\n")
        f.write("    }\n\n")

        f.write(r"""
    estado_actual = 'A'
    lexema = ''
    tokens = []
    i = 0

    while i < len(texto):
        c = texto[i]
        if (estado_actual, c) in transitions:
            estado_actual = transitions[(estado_actual, c)]
            lexema += c
            i += 1
        else:
            if estado_actual in accepting:
                tokens.append((lexema, accepting[estado_actual]))
                estado_actual = 'A'
                lexema = ''
            elif lexema:
                tokens.append((lexema, 'ERROR'))
                estado_actual = 'A'
                lexema = ''
            else:
                tokens.append((c, 'ERROR'))
                i += 1

    if lexema:
        if estado_actual in accepting:
            tokens.append((lexema, accepting[estado_actual]))
        else:
            tokens.append((lexema, 'ERROR'))

    return tokens

if __name__ == '__main__':
    with open('input/codigo.txt', 'r', encoding='utf-8') as file:
        contenido = file.read()
        resultado = analizar(contenido)
        for lexema, token in resultado:
            print(f"{lexema} -> {token}")
""")

    print(f"✅ lexer.py generado en: {ruta_salida}")
