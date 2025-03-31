def expandir_definiciones(data):
    definiciones = data['definitions']
    tokens = data['tokens']

    def remove_quotes(s):
        s = s.strip()
        if (s.startswith("'") and s.endswith("'")) or (s.startswith('"') and s.endswith('"')):
            return s[1:-1]
        return s

    def expand(expr):
        expr = expr.strip()
        expr = replace_definitions(expr)
        expr = expand_brackets(expr)
        expr = escape_specials(expr)
        return expr

    def replace_definitions(expr):
        changed = True
        while changed:
            changed = False
            for nombre, definicion in definiciones.items():
                if nombre in expr:
                    new_expr = ''
                    i = 0
                    while i < len(expr):
                        if expr[i:i+len(nombre)] == nombre:
                            new_expr += f"({replace_definitions(definicion)})"
                            i += len(nombre)
                            changed = True
                        else:
                            new_expr += expr[i]
                            i += 1
                    expr = new_expr
        return expr

    def expand_brackets(expr):
        result = ''
        i = 0
        while i < len(expr):
            if expr[i] == '[':
                j = i + 1
                content = ''
                while j < len(expr) and expr[j] != ']':
                    content += expr[j]
                    j += 1
                expanded = expand_char_class(content)
                result += f'({expanded})'
                i = j + 1  # saltar el ']'
            else:
                result += expr[i]
                i += 1
        return result
    
    def expand_range(start, end) -> list:
        return [chr(c) for c in range(ord(start), ord(end) + 1)]



    def expand_char_class(content):
        i = 0
        chars = []
        while i < len(content):
            # Saltar espacios extra (pero no descartar un literal que sea un espacio)
            while i < len(content) and content[i].isspace():
                i += 1
            if i < len(content) and content[i] == "'":
                # Primero, intentamos detectar un rango del tipo: 'X'-'Y'
                if (i + 6 < len(content) and
                    content[i] == "'" and content[i+2] == "'" and 
                    content[i+3] == '-' and content[i+4] == "'" and 
                    content[i+6] == "'"):
                    start = content[i+1]
                    end = content[i+5]
                    chars.extend(expand_range(start, end))
                    i += 7

                else:
                    # Si no es rango, extraemos el literal entre comillas
                    j = i + 1
                    literal = ""
                    while j < len(content) and content[j] != "'":
                        literal += content[j]
                        j += 1
                    if j < len(content) and content[j] == "'":
                        # Manejo de secuencias escapadas
                        if literal == "\\t":
                            literal = "\t"
                        elif literal == "\\n":
                            literal = "\n"
                        # No aplicamos strip() para conservar un espacio literal
                        chars.append(literal)
                    i = j + 1
            else:
                i += 1
        return '|'.join(chars)



    def escape_specials(expr):
        return expr  # ya no hacemos escapes aquí



    tokens_expandidos = []
    for raw_expr, token in tokens:
        # (Procesamiento: remove_quotes, replace_definitions, expand_brackets, etc.)
        # Por ejemplo:
        cleaned = remove_quotes(raw_expr)
        if cleaned == '':
            print(f"⚠️  Literal vacío para token '{token}', se omite.")
            continue

        if raw_expr[0] in {"'", '"'} and len(remove_quotes(raw_expr)) == 1:
            # Para tokens literales (como '+' o '*') antepone una barra para que
            # se traten como caracteres y no como operadores en la fase de tokenización
            ex = '\\' + remove_quotes(raw_expr)
        elif cleaned in definiciones:
            ex = expand(cleaned)
        else:
            ex = expand(cleaned)
        tokens_expandidos.append((ex, token))
        print(f"  ✔ Token={token}, Regex expandida='{ex}'")
    
    return tokens_expandidos