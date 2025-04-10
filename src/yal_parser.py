def leerYAL(ruta):
    """
    Parser que maneja un archivo .yal line by line.
    Reconoce:
      - header opcional { ... } en una línea.
      - definiciones let x = ...
      - rule <name> [args] = ...
        line tokens (regex { action })
      - trailer opcional { ... }
    """
    lines = []
    with open(ruta, 'r', encoding='utf-8') as f:
        for raw in f:
            clean = quitar_comentarios(raw)
            if my_trim(clean):
                lines.append(my_trim(clean))

    idx = 0
    header = None
    trailer = None
    definitions = {}
    rules = []

    # 1) header opcional
    idx, header = parse_optional_brace_block_in_lines(lines, idx)

    # 2) definiciones let
    while idx < len(lines):
        line = lines[idx]
        # Usamos my_trim para evaluar el comienzo de la línea
        if my_trim(line).startswith('rule '):
            break
        if my_trim(line).startswith('let '):
            nombre, regexp = parse_let_line(line)
            definitions[nombre] = regexp
            idx += 1
        else:
            break

    # 3) rules
    while idx < len(lines):
        line = lines[idx]
        if my_trim(line).startswith('rule '):
            rule_name, rule_args = parse_rule_declaration(line)
            idx += 1
            rule_tokens = []
            while idx < len(lines):
                l2 = lines[idx]
                if not l2 or my_trim(l2).startswith('rule ') or my_trim(l2).startswith('let ') or my_trim(l2).startswith('{'):
                    break

                if my_trim(l2).startswith('|'):
                    # Se elimina el '|' y se aplica my_trim
                    l2 = my_trim(l2[1:])

                reg, act = parse_regex_action_line(l2)
                rule_tokens.append((reg, act))
                idx += 1

            rules.append({
                'name': rule_name,
                'args': rule_args,
                'tokens': rule_tokens
            })
        elif my_trim(line).startswith('{'):
            break
        else:
            break

    # 4) trailer
    idx, trailer = parse_optional_brace_block_in_lines(lines, idx)

    # aplanar tokens
    all_tokens = []
    for r in rules:
        for (rg, act) in r['tokens']:
            all_tokens.append((rg, act))

    return {
        'header': header,
        'trailer': trailer,
        'definitions': definitions,
        'rules': rules,
        'tokens': all_tokens
    }


def my_trim(s: str) -> str:
    whitespace = " \t\n\r"
    start = 0
    end = len(s)
    while start < end and s[start] in whitespace:
        start += 1
    while end > start and s[end - 1] in whitespace:
        end -= 1
    return s[start:end]

# Otras funciones auxiliares

def quitar_comentarios(line: str) -> str:
    """
    Elimina (* ... *) en una sola línea, si los hay.
    """
    out = ''
    i = 0
    inside = False
    while i < len(line):
        if not inside and line[i:i+2] == '(*':
            inside = True
            i += 2
        elif inside and line[i:i+2] == '*)':
            inside = False
            i += 2
        else:
            if not inside:
                out += line[i]
            i += 1
    return out

def parse_optional_brace_block_in_lines(lines, idx):
    if idx < len(lines):
        line = my_trim(lines[idx])
        if line.startswith('{') and line.endswith('}'):
            content = my_trim(line[1:-1])
            idx += 1
            return idx, content
    return idx, None

def parse_let_line(line: str):
    # e.g. "let ws = delim+"
    rest = my_trim(line[4:])  # quitar 'let ' y limpiar
    if '=' in rest:
        nombre, regexp = rest.split('=', 1)
        return my_trim(nombre), my_trim(regexp)
    return '???', ''

def parse_rule_declaration(line: str):
    # e.g. "rule tokens =" o "rule tokens [args] ="
    rest = my_trim(line[5:])  # quitar 'rule ' y limpiar
    name = ''
    args = []
    if '[' in rest:
        ib = rest.index('[')
        name = my_trim(rest[:ib])
        jb = rest.index(']', ib)
        inside = my_trim(rest[ib+1:jb])
        args = inside.split()
        # si hay '=', se ignora
    else:
        if '=' in rest:
            eqpos = rest.index('=')
            name = my_trim(rest[:eqpos])
        else:
            name = rest
    return name, args

def parse_regex_action_line(line: str):
    """
    Separa la parte 'regex { action }'
    o la parte 'regex' sin action.
    """
    if '{' in line and '}' in line:
        ib = line.index('{')
        reg = my_trim(line[:ib])
        after = line[ib+1:]
        jb = after.index('}')
        act_part = my_trim(after[:jb])
        token = parse_return_token(act_part)
        return reg, token
    else:
        return my_trim(line), None

def parse_return_token(s: str) -> str:
    """
    Si hay 'return X', devuelve X
    """
    words = s.split()
    if 'return' in words:
        i = words.index('return')
        if i + 1 < len(words):
            return words[i + 1]
    return None
