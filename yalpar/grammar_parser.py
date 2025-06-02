# yalpar/grammar_parser.py

def quitar_comentarios(texto):
    resultado = []
    i = 0
    n = len(texto)
    while i < n:
        # Si encontramos inicio de comentario '/*', saltamos hasta '*/'
        if i + 1 < n and texto[i] == '/' and texto[i+1] == '*':
            i += 2
            # Avanzar hasta encontrar '*/' o llegar al final
            while i + 1 < n and not (texto[i] == '*' and texto[i+1] == '/'):
                i += 1
            # Si encontramos '*/', salta esos dos caracteres también
            if i + 1 < n:
                i += 2
        else:
            # No es inicio de comentario, conservar el carácter
            resultado.append(texto[i])
            i += 1
    return "".join(resultado)


def parse_yalp(filepath):
    # 1) Leer todo el archivo como texto
    with open(filepath, 'r', encoding='utf-8') as f:
        texto = f.read()

    # 2) Quitar comentarios /* ... */
    texto_sin_comentarios = quitar_comentarios(texto)

    # 3) Dividir en líneas, descartando las líneas vacías y espacios sobrantes
    lines = []
    for raw_line in texto_sin_comentarios.splitlines():
        line = raw_line.strip()
        if line:
            lines.append(line)

    tokens = set()
    non_terminals = set()
    productions = []
    start_symbol = None

    # 4) Leer la sección de %token ...
    i = 0
    while i < len(lines) and lines[i].startswith('%token'):
        # Ejemplo: "%token ID NUMBER PLUS MINUS"
        partes = lines[i].split()
        for tok in partes[1:]:
            tokens.add(tok)  # guardamos cada token en mayúscula
        i += 1

    # 5) Mapa de literales a tokens (en mayúscula)
    literal_map = {
        ';': 'SEMICOLON',
        '<': 'LT',
        'eq': 'EQ',
    }

    # 6) Leer producciones: cada línea que contenga ':' define un LHS → varias RHS
    while i < len(lines):
        line = lines[i]
        if ':' not in line:
            i += 1
            continue

        # 6.a) Extraer LHS (parte antes de ':') y pasarlo a minúscula
        lhs_raw = line.split(':', 1)[0].strip()
        lhs = lhs_raw.lower()
        if start_symbol is None:
            start_symbol = lhs
        non_terminals.add(lhs)

        # 6.b) Construir la parte RHS (podría abarcar varias líneas hasta ';')
        rhs_part = line.split(':', 1)[1].strip()
        i += 1
        # Mientras no termine la parte RHS con ';', concatenamos la siguiente línea
        while not rhs_part.endswith(';') and i < len(lines):
            rhs_part += ' ' + lines[i].strip()
            i += 1

        # Ahora rhs_part termina en ';'. Eliminamos ese ';' final.
        rhs_text = rhs_part[:-1].strip()  # Quita el “;”
        # Dividir por alternativas con '|'
        alternativas = [alt.strip() for alt in rhs_text.split('|')]

        for alt in alternativas:
            # Cada alt es algo como "expression PLUS term" o "term"
            símbolos = alt.split()
            rhs_normalizado = []
            for sym in símbolos:
                # 1) Si sym coincide exactamente con alguno de los tokens en mayúscula:
                if sym in tokens:
                    rhs_normalizado.append(sym)
                    continue

                # 2) Si sym en minúscula coincide con un non_terminal que ya conocemos:
                sym_min = sym.lower()
                if sym_min in non_terminals:
                    rhs_normalizado.append(sym_min)
                    continue

                # 3) Si sym.upper() coincide con un token (p. ej. 'eq' → 'EQ'):
                up = sym.upper()
                if up in tokens:
                    rhs_normalizado.append(up)
                    continue

                # 4) Si sym corresponde a uno de los literales mapeados:
                if sym in literal_map:
                    rhs_normalizado.append(literal_map[sym])
                    continue

                # 5) Si no encaja en ninguno de los casos anteriores, tratamos sym como
                #    un nuevo no-terminal (en minúscula).
                rhs_normalizado.append(sym_min)
                non_terminals.add(sym_min)

            productions.append((lhs, rhs_normalizado))

    if start_symbol is None:
        raise RuntimeError(f"El archivo {filepath} no define ninguna producción (no encontró ':').")

    return {
        'tokens': tokens,
        'non_terminals': non_terminals,
        'productions': productions,
        'start_symbol': start_symbol
    }


if __name__ == '__main__':
    import pprint, sys
    if len(sys.argv) != 2:
        print("Uso: python grammar_parser.py <archivo.yalp>")
        sys.exit(1)
    ruta = sys.argv[1]
    try:
        gram = parse_yalp(ruta)
        pprint.pprint(gram)
    except Exception as e:
        print("Error al parsear:", e)
