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
            if clean.strip():
                lines.append(clean.strip())

    idx = 0
    header = None
    trailer = None
    definitions = {}
    rules = []

    # 1) header optional
    idx, header = parse_optional_brace_block_in_lines(lines, idx)

    # 2) definiciones let
    while idx < len(lines):
        line = lines[idx]
        if line.startswith('rule '):
            break
        if line.startswith('let '):
            nombre, regexp = parse_let_line(line)
            definitions[nombre] = regexp
            idx += 1
        else:
            # no let => paramos
            break

    # 3) rules
    while idx < len(lines):
        line = lines[idx]
        if line.startswith('rule '):
            # parse rule
            rule_name, rule_args = parse_rule_declaration(line)
            idx += 1
            # leemos lineas hasta toparse con rule, let, '{', o fin
            rule_tokens = []
            while idx < len(lines):
                l2 = lines[idx]
                if not l2 or l2.startswith('rule ') or l2.startswith('let ') or l2.startswith('{'):
                    # salimos
                    break

                # si la linea empieza con '|', se la quitamos
                # asi "| id { return ID }" => "id { return ID }"
                if l2.startswith('|'):
                    l2 = l2[1:].strip()

                # parse regex y action
                reg, act = parse_regex_action_line(l2)
                rule_tokens.append((reg, act))
                idx += 1

            rules.append({
                'name': rule_name,
                'args': rule_args,
                'tokens': rule_tokens
            })
        elif line.startswith('{'):
            # quizas trailer
            break
        else:
            # nada => break
            break
    # fin while

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

############################
# Auxiliares
############################

def quitar_comentarios(line:str)->str:
    """
    Elimina (* ... *) en una sola línea, si los hay.
    """
    out=''
    i=0
    inside=False
    while i<len(line):
        if not inside and line[i:i+2]=='(*':
            inside=True
            i+=2
        elif inside and line[i:i+2]=='*)':
            inside=False
            i+=2
        else:
            if not inside:
                out+=line[i]
            i+=1
    return out

def parse_optional_brace_block_in_lines(lines, idx):
    if idx<len(lines):
        line=lines[idx].strip()
        if line.startswith('{') and line.endswith('}'):
            content=line[1:-1].strip()
            idx+=1
            return idx, content
    return idx, None

def parse_let_line(line:str):
    # e.g. "let ws = delim+"
    rest=line[4:].strip()  # quitar 'let '
    if '=' in rest:
        nombre,regexp=rest.split('=',1)
        return nombre.strip(), regexp.strip()
    return '???',''

def parse_rule_declaration(line:str):
    # e.g. "rule tokens ="
    # or "rule tokens [args] ="
    rest=line[5:].strip()  # quita 'rule '
    name=''
    args=[]
    if '[' in rest:
        ib=rest.index('[')
        name=rest[:ib].strip()
        jb=rest.index(']',ib)
        inside=rest[ib+1:jb].strip()
        args=inside.split()
        # si hay '='
        if '=' in rest[jb:]:
            # ignoring
            pass
    else:
        # no bracket
        # check if '='
        if '=' in rest:
            eqpos=rest.index('=')
            name=rest[:eqpos].strip()
        else:
            name=rest
    return name,args

def parse_regex_action_line(line:str):
    """
    Separa la parte 'regex { action }'
    o la parte 'regex' sin action.
    """
    if '{' in line and '}' in line:
        ib=line.index('{')
        reg=line[:ib].strip()
        after=line[ib+1:]
        jb=after.index('}')
        act_part=after[:jb].strip()
        token= parse_return_token(act_part)
        return reg, token
    else:
        # no action
        return line.strip(), None

def parse_return_token(s:str)->str:
    """
    Si hay 'return X', devolvemos X
    """
    words=s.split()
    if 'return' in words:
        i=words.index('return')
        if i+1<len(words):
            return words[i+1]
    return None
