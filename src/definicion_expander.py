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
        expr = escape_literals(expr)
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
        i = 0
        result = ''
        while i < len(expr):
            if expr[i] == '[':
                j = i + 1
                content = ''
                while j < len(expr) and expr[j] != ']':
                    content += expr[j]
                    j += 1
                expanded = expand_char_class(content)
                result += f'({expanded})'
                i = j + 1
            else:
                result += expr[i]
                i += 1
        return result

    def expand_char_class(content):
        i = 0
        chars = []
        while i < len(content):
            if i+2 < len(content) and content[i+1] == '-':
                start = content[i]
                end = content[i+2]
                chars.extend([chr(c) for c in range(ord(start), ord(end)+1)])
                i += 3
            elif content[i] == "'" and i+2 < len(content) and content[i+2] == "'":
                chars.append(content[i+1])
                i += 3
            else:
                chars.append(content[i])
                i += 1
        return '|'.join(chars)

    def escape_literals(expr):
        """
        Escapa operadores y paréntesis si están fuera de comillas
        """
        escaped = ''
        special = {'.', '*', '+', '?', '(', ')', '|'}
        i = 0
        while i < len(expr):
            c = expr[i]
            if c in special:
                escaped += f"\\{c}"
            else:
                escaped += c
            i += 1
        return escaped

    tokens_expandidos = []
    for raw_expr, token in tokens:
        cleaned = remove_quotes(raw_expr)
        if cleaned == '':
            print(f"⚠️  Literal vacío para token '{token}', se omite.")
            continue
        ex = expand(cleaned)
        tokens_expandidos.append((ex, token))
        print(f"  ✔ Token={token}, Regex expandida='{ex}'")

    return tokens_expandidos
