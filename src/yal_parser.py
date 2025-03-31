# yal_parser.py

def leerYAL(ruta):
    """
    Parser que maneja un archivo .yal en varios estados:
      - header opcional { ... }
      - definiciones let
      - rules (cada rule con tokens)
      - trailer opcional { ... }

    Retorna un dict con:
      {
        'header': str or None,
        'trailer': str or None,
        'definitions': {nombre: regexp, ...},
        'rules': [
          {
            'name': ...,
            'args': [...],
            'tokens': [
              (regex, action), ...
            ]
          }, ...
        ],
        'tokens': [ (regex, action), ... ]  # aplanado
      }
    """
    # 1) Leer el archivo, quitar comentarios, y almacenar líneas limpias
    lines = []
    with open(ruta, 'r', encoding='utf-8') as f:
        for raw in f:
            clean = quitar_comentarios(raw)
            if clean.strip():
                lines.append(clean.strip())

    # 2) Modo: leer header opcional
    idx = 0
    header = None
    trailer = None
    definitions = {}
    rules = []  # cada rule: {'name':..., 'args':..., 'tokens':[...]}

    # Intentamos ver si la primera línea (o varias) es un bloque { ... }
    idx, header = parse_optional_brace_block_in_lines(lines, idx)

    # 3) Leer definiciones let ... = ...
    while idx < len(lines):
        line = lines[idx]
        if line.startswith('rule '):
            # Pasamos a rules
            break
        if line.startswith('let '):
            # parse definicion
            # Ej: let nombre = loquesea
            # se hace parse suelto en la misma linea
            # o si hay algo multiline? Asumimos la definicion entera está en la línea
            nombre, regexp = parse_let_line(line)
            definitions[nombre] = regexp
            idx += 1
        else:
            # no let ni rule => salimos
            idx += 1
            break

    # 4) Leer rules
    while idx < len(lines):
        line = lines[idx]
        if line.startswith('rule '):
            # parse rule name, args
            rule_name, rule_args = parse_rule_declaration(line)
            idx += 1
            # luego leemos las lineas de tokens hasta vacio o nueva 'rule ' o '{...}'
            rule_tokens = []
            while idx < len(lines):
                l2 = lines[idx]
                if l2.startswith('rule ') or l2.startswith('let ') or l2.startswith('{') or not l2:
                    break
                # parse "regex {action}" o lines con '|'
                # una linea tipica:
                #  ws
                # o
                #  id { return ID }
                # Con pipeline se juntan con '|'. Pero tu parser original permitía multiline
                # nosotros parseamos cada line. 
                # Checar si hay '{'...
                if '{' in l2 and '}' in l2:
                    # parse
                    reg, act = parse_regex_action_line(l2)
                    rule_tokens.append((reg, act))
                else:
                    # puede ser una regex sin action
                    # o puede ser un token sin llaves?
                    # tu .yal a veces pone algo como:
                    #  ws
                    # => no action
                    reg = l2
                    act = None
                    rule_tokens.append((reg, act))
                idx += 1

            rules.append({
                'name': rule_name,
                'args': rule_args,
                'tokens': rule_tokens
            })
        elif line.startswith('{'):
            # Podría ser trailer
            break
        else:
            # no es rule => break
            break
        # si no break, continue
    # fin while rules

    # 5) Trailer
    idx, trailer = parse_optional_brace_block_in_lines(lines, idx)

    # 6) Aplanar tokens
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

#############################
# FUNCIONES AUXILIARES
#############################

def quitar_comentarios(line: str)->str:
    """
    Elimina los (* ... *) en una sola línea.
    No soporta multiline (depende de tu .yal).
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
    """
    Si la linea actual (u otra) inicia con '{',
    capturamos todo hasta '}' en la misma linea
    (asumiendo no multiline).
    Retornamos (nuevo_idx, contenido) o (idx, None).
    """
    if idx<len(lines):
        line=lines[idx]
        line=line.strip()
        if line.startswith('{') and line.endswith('}'):
            # tomamos su contenido
            content=line[1:-1].strip()
            idx+=1
            return idx, content
    return idx, None

def parse_let_line(line: str):
    """
    parse 'let nombre = regexp'.
    Suponemos que cabe en la misma linea.
    """
    # remover 'let '
    rest=line[4:].strip()
    # splitted by '='
    if '=' in rest:
        partes=rest.split('=',1)
        nombre=partes[0].strip()
        regexp=partes[1].strip()
    else:
        # error
        nombre='???'
        regexp=''
    return nombre, regexp

def parse_rule_declaration(line: str):
    """
    parsea algo como:
    rule tokens [args] =
    Devolvemos (tokens, [args]).
    Asumimos que la parte final '=' puede estar o no.
    """
    # remove 'rule '
    rest=line[5:].strip()
    # si hay '[' => parse name, y lo que hay en '[]'
    # sino => parse name
    name=''
    args=[]
    if '[' in rest:
        # e.g. tokens [ arg1 arg2 ] =
        i=rest.index('[')
        name=rest[:i].strip()
        j=rest.index(']',i)
        inside=rest[i+1:j].strip()
        args=inside.split()
        # si hay '=' => ignorarlo
        # ...
    else:
        # no brackets
        # si hay '=' => remove
        if '=' in rest:
            eqpos=rest.index('=')
            name=rest[:eqpos].strip()
        else:
            name=rest
    return name,args

def parse_regex_action_line(line:str):
    """
    parsea algo del tipo:
    id { return ID }
    number { return NUMBER }
    o
    ws
    """
    # si no hay '{' => no action
    if '{' not in line:
        return line.strip(), None
    # splitted
    # e.g. "id { return ID }"
    idx=line.index('{')
    reg=line[:idx].strip()
    after=line[idx+1:]
    if '}' in after:
        idx2=after.index('}')
        act=after[:idx2].strip()
        # parse return token
        token= parse_return_token(act)
        return reg, token
    else:
        # no cierra
        return reg,None

def parse_return_token(action_str:str):
    """
    Si hay 'return X', devolvemos X
    """
    words=action_str.split()
    if 'return' in words:
        i=words.index('return')
        if i+1<len(words):
            return words[i+1]
    return None

def saltar_espacios(data:str, idx:int)->int:
    while idx<len(data) and data[idx].isspace():
        idx+=1
    return idx

def parse_until_keyword(data, idx, stop_keywords=None):
    """
    Originalmente usado en tu parser unificado. 
    No lo necesitamos con line-by-line approach,
    pero lo dejamos si se usa. 
    """
    if stop_keywords is None:
        stop_keywords=[]
    start=idx
    length=len(data)
    while idx<length:
        for kw in stop_keywords:
            if data.startswith(kw,idx):
                return data[start:idx], idx
        idx+=1
    return data[start:], idx

def parse_until_char(data, idx, char):
    """
    Originalmente usado en tu parser unificado. 
    No lo necesitamos con line-by-line approach,
    pero lo dejamos si se usa. 
    """
    start=idx
    length=len(data)
    while idx<length and data[idx]!=char:
        idx+=1
    return data[start:idx], idx
