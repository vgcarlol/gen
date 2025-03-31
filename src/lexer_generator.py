# lexer_generator.py
import os

def generar_lexer_py(afd, token_map, ruta_salida="output/lexer.py"):
    os.makedirs(os.path.dirname(ruta_salida), exist_ok=True)

    with open(ruta_salida, "w", encoding="utf-8") as f:
        f.write("""# AUTO-GENERADO: Analizador léxico basado en AFD

def analizar(texto):
    transitions = {
""")

        for (estado, simbolo), destino in afd.getTransitions().items():
            estado_str = repr(estado)
            simbolo_str = repr(simbolo)
            destino_str = repr(destino)
            f.write(f"        ({estado_str}, {simbolo_str}): {destino_str},\n")

        f.write("    }\n\n")

        f.write("    accepting = {\n")
        if hasattr(afd, "accepting_map"):
            for estado, (_, token_name) in afd.accepting_map.items():
                f.write(f"        {repr(estado)}: {repr(token_name)},\n")
        f.write("    }\n\n")

        f.write(r"""
    estado_inicial = 'A'
    tokens = []
    i = 0
    while i < len(texto):
        estado_actual = estado_inicial
        lexema = ''
        ultimo_token = None
        ultimo_index = i

        j = i
        while j < len(texto):
            c = texto[j]
            if (estado_actual, c) in transitions:
                estado_actual = transitions[(estado_actual, c)]
                lexema += c
                if estado_actual in accepting:
                    ultimo_token = (lexema, accepting[estado_actual])
                    ultimo_index = j + 1
                j += 1
            else:
                break

        if ultimo_token:
            tokens.append(ultimo_token)
            i = ultimo_index
        else:
            tokens.append((texto[i], 'ERROR'))
            i += 1

    return tokens

if __name__ == '__main__':
    with open('input/codigo.txt', 'r', encoding='utf-8') as file:
        contenido = file.read()
        resultado = analizar(contenido)

    with open('output/tokens.txt', 'w', encoding='utf-8') as out:
        for lexema, token in resultado:
            out.write(f"{lexema} -> {token}\n")
""")

    print(f"✅ lexer.py generado en: {ruta_salida}")
