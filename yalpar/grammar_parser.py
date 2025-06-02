# yalpar/grammar_parser.py

import re

def parse_yalp(filepath):
    """
    Lee un archivo .yalp y devuelve un diccionario con:
      - tokens (set de strings, en mayúscula)
      - non_terminals (set de strings, en minúscula)
      - productions (lista de tuplas: (lhs_minúscula, [símbolos_rhs_normalizados]))
      - start_symbol (string en minúscula)
    
    Estrategia de normalización:
      • Los tokens se guardan tal cual aparecen en %token (en mayúscula).
      • Todos los no-terminales se almacenan en minúscula.
      • Cada vez que en las producciones aparezca un símbolo en mayúscula que 
        coincida (ignorando mayúsculas/minúsculas) con un no-terminal, se convierte 
        a su versión en minúscula.
      • Se mapea también los literales “;”, “<” y “eq” a sus tokens correspondientes 
        (en mayúscula).
    """
    # 1) Leemos el contenido y eliminamos comentarios estilo C (/* ... */).
    with open(filepath, 'r', encoding='utf-8') as f:
        texto = f.read()
    texto_sin_comentarios = re.sub(r'/\*.*?\*/', '', texto, flags=re.DOTALL)

    # 2) Partimos en líneas y descartamos vacías.
    lines = [line.strip() for line in texto_sin_comentarios.splitlines() if line.strip()]

    tokens = set()
    non_terminals = set()
    productions = []
    start_symbol = None

    # 3) Leer la sección de %token ...
    i = 0
    while i < len(lines) and lines[i].startswith('%token'):
        # Ejemplo: "%token ID NUMBER PLUS MINUS"
        partes = lines[i].split()
        for tok in partes[1:]:
            tokens.add(tok)  # guardamos en mayúscula
        i += 1

    # 4) Mapa de literales a tokens (en mayúscula)
    literal_map = {
        ';': 'SEMICOLON',
        '<': 'LT',
        'eq': 'EQ',
    }

    # 5) Leer producciones: cada vez que encontramos “:” interpretamos LHS → RHS ;
    while i < len(lines):
        line = lines[i]
        if ':' not in line:
            i += 1
            continue

        # LHS es toda la parte antes de “:”. Lo normalizamos a minúscula:
        lhs_raw = line.split(':', 1)[0].strip()
        lhs = lhs_raw.lower()
        if start_symbol is None:
            start_symbol = lhs
        non_terminals.add(lhs)

        # Construir la parte RHS concatenando líneas si hace falta hasta el “;”
        rhs_part = line.split(':', 1)[1].strip()
        i += 1
        while not rhs_part.endswith(';') and i < len(lines):
            rhs_part += ' ' + lines[i].strip()
            i += 1

        # Quitar el “;” final para quedarnos solo con las alternativas
        rhs_text = rhs_part[:-1].strip()  # quita el “;”
        alternativas = [alt.strip() for alt in rhs_text.split('|')]

        for alt in alternativas:
            símbolos = alt.split()
            rhs_normalizado = []
            for sym in símbolos:
                # Si sym es un token explícito en mayúscula: lo aceptamos tal cual.
                if sym in tokens:
                    rhs_normalizado.append(sym)
                    continue

                # Si sym (en minúscula) está en nuestro conjunto de no_terminals: lo usamos.
                sym_min = sym.lower()
                if sym_min in non_terminals:
                    rhs_normalizado.append(sym_min)
                    continue

                # Si al convertir sym a mayúscula obtenemos un token válido:
                up = sym.upper()
                if up in tokens:
                    rhs_normalizado.append(up)
                    continue

                # Si sym aparece en literal_map (ej. ‘;’ → SEMICOLON, ‘<’ → LT, ‘eq’ → EQ):
                if sym in literal_map:
                    rhs_normalizado.append(literal_map[sym])
                    continue

                # Finalmente, si no es ni token ni lit ni LHS conocido, lo asumimos como no_terminal
                # (probablemente la primera vez que aparece); lo agregamos en minúscula.
                rhs_normalizado.append(sym_min)
                non_terminals.add(sym_min)

            productions.append((lhs, rhs_normalizado))

    if start_symbol is None:
        raise RuntimeError(f"El archivo {filepath} no define ninguna producción (no halló ':').")

    return {
        'tokens': tokens,
        'non_terminals': non_terminals,
        'productions': productions,
        'start_symbol': start_symbol
    }


if __name__ == '__main__':
    # Pequeña prueba para ver qué se generó
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
