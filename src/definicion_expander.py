import string

def is_id_char(c):
    # Consideramos como caracter de identificador: letras (mayúsculas y minúsculas), dígitos y '_'
    return c in string.ascii_letters + string.digits + "_"

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
        # Iterar sobre las definiciones ordenadas de mayor a menor longitud
        definiciones_ordenadas = sorted(definiciones.items(), key=lambda item: len(item[0]), reverse=True)
        while changed:
            changed = False
            new_expr = ''
            i = 0
            while i < len(expr):
                replaced = False
                for nombre, definicion in definiciones_ordenadas:
                    if expr[i:i+len(nombre)] == nombre:
                        left_ok = (i == 0) or (not is_id_char(expr[i-1]))
                        right_ok = (i+len(nombre) == len(expr)) or (not is_id_char(expr[i+len(nombre)]))
                        if left_ok and right_ok:
                            new_expr += f"({replace_definitions(definicion)})"
                            i += len(nombre)
                            changed = True
                            replaced = True
                            break
                if not replaced:
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
                result += expanded 
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

        # CASO NUEVO: ["0123456789"]
        if content.startswith('"') and content.endswith('"') and len(content) > 2:
            content = content[1:-1]  # quitar las comillas externas
            for c in content:
                chars.append(c)
        else:
            # Si es una clase tipo ["0123456789"]
            if content.startswith('"') and content.endswith('"'):
                return '(' + '|'.join(content[1:-1]) + ')'

            while i < len(content):
                if content[i] == "'" and (i + 2 < len(content)) and content[i+2] == "'":
                    literal = content[i+1]
                    i += 3
                    if i + 4 <= len(content) and content[i] == '-' and content[i+1] == "'" and content[i+3] == "'":
                        end_char = content[i+2]
                        chars.extend(expand_range(literal, end_char))
                        i += 4
                    else:
                        chars.append(literal)
                elif content[i] == '\\':
                    if i + 1 < len(content):
                        escape_char = content[i + 1]
                        if escape_char == 'n':
                            chars.append('\n')
                        elif escape_char == 't':
                            chars.append('\t')
                        elif escape_char == 'r':
                            chars.append('\r')
                        elif escape_char == '\\':
                            chars.append('\\')
                        else:
                            chars.append('\\' + escape_char)
                        i += 2
                    else:
                        chars.append('\\')
                        i += 1
                elif content[i] == ' ':
                    chars.append(' ')
                    i += 1
                else:
                    chars.append(content[i])
                    i += 1

        def escape_special(c):
            if c == '\n':
                return r'\n'
            elif c == '\t':
                return r'\t'
            elif c == '\r':
                return r'\r'
            elif c == ' ':
                return ' '
            elif c in {'+', '-', '*', '?', '|', '(', ')', '.', '[', ']', '{', '}', '\\'}:
                return '\\' + c
            return c

        return '(' + '|'.join(escape_special(c) for c in chars) + ')'



    def escape_specials(expr):
        return expr  # ya no hacemos escapes aquí


    from regex_functions import formatRegex

    tokens_expandidos = []
    for raw_expr, token in tokens:
        cleaned = remove_quotes(raw_expr)
        if cleaned == '':
            print(f"⚠️  Literal vacío para token '{token}', se omite.")
            continue

        # 🚨 Caso especial: WHITESPACE
        if token == "WHITESPACE":
            ex = '(\n|\t| )+'

        elif raw_expr[0] in {"'", '"'} and len(remove_quotes(raw_expr)) == 1:
            val = remove_quotes(raw_expr)
            # Si es un carácter especial que necesita escape en regex, escápalo
            if val in {'.', '*', '+', '?', '(', ')', '[', ']', '{', '}', '\\', '|', '^', '$'}:
                ex = '\\' + val
            elif val == 'n':
                ex = '\n'
            elif val == 't':
                ex = '\t'
            elif val == 'r':
                ex = '\r'
            else:
                ex = val

        else:
            ex = expand(cleaned.replace("'", "").replace('"', ''))

        # Aplicamos postprocesamiento
        # Escapamos signos que deben ser tratados como literales si están solos
        ex = ex.replace('(+|-)', r'(\+|\-)')
        ex = formatRegex(ex)
        tokens_expandidos.append((ex, token))
        print(f"  ✔ Token={token}, Regex expandida='{ex}'")

        
    return tokens_expandidos