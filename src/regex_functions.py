# regex_functions.py

from utilidades import Stack

def leerArchivo():
    """
    Lee expresiones desde input/expressions.txt (opcional en tu proyecto).
    """
    with open("input/expressions.txt", "r", encoding='utf-8') as archivo:
        lineas = archivo.readlines()
    
    expresiones_regulares = []
    for linea in lineas:
        linea = linea.strip()
        if not linea or linea.startswith("#"):
            continue
        if validarExpresion(linea):
            expresiones_regulares.append(linea)
        else:
            print(f"Expresión inválida detectada y omitida: {linea}")
    return expresiones_regulares

def parseRegex(tokens: list):
    """
    Construye el AST a partir de la lista de tokens.
    Se espera que 'tokens' provenga de tokenizeRegex(expanded),
    sin pasar por insertConcat.
    """
    index = 0  # índice de tokens

    def current():
        return tokens[index]

    def eat(token_type=None):
        nonlocal index
        tok = tokens[index]
        index += 1
        if token_type and tok.type != token_type:
            raise ValueError(f"Se esperaba {token_type}, pero se obtuvo {tok.type}")
        return tok

    def parse_union():
        node = parse_concat()
        while index < len(tokens) and tokens[index].type == T_UNION:
            eat(T_UNION)
            right = parse_concat()
            node = UnionNode(node, right)
        return node

    def parse_concat():
        node = parse_repeat()
        # Mientras el siguiente token sea candidato a comenzar un operando
        while index < len(tokens) and tokens[index].type in {T_CHAR, T_LPAREN}:
            right = parse_repeat()
            node = ConcatNode(node, right)
        return node

    def parse_repeat():
        node = parse_primary()
        while index < len(tokens) and tokens[index].type in {T_STAR, T_PLUS, T_QUESTION}:
            op = eat()
            if op.type == T_STAR:
                node = StarNode(node)
            elif op.type == T_PLUS:
                node = PlusNode(node)
            elif op.type == T_QUESTION:
                node = QuestionNode(node)
        return node

    def parse_primary():
        tok = tokens[index]
        if tok.type == T_CHAR:
            eat(T_CHAR)
            return LiteralNode(tok.val)
        elif tok.type == T_LPAREN:
            eat(T_LPAREN)
            node = parse_union()
            eat(T_RPAREN)
            return node
        else:
            raise ValueError(f"Token inesperado en primary: {tok}")

    ast = parse_union()
    return ast

def astToPostfix(ast: "RegexNode") -> list:
    result = []
    def traverse(node):
        if isinstance(node, LiteralNode):
            result.append(Token(T_CHAR, node.value))
        elif isinstance(node, ConcatNode):
            traverse(node.left)
            traverse(node.right)
            result.append(Token(T_CONCAT))
        elif isinstance(node, UnionNode):
            traverse(node.left)
            traverse(node.right)
            result.append(Token(T_UNION))
        elif isinstance(node, StarNode):
            traverse(node.child)
            result.append(Token(T_STAR))
        elif isinstance(node, PlusNode):
            traverse(node.child)
            result.append(Token(T_PLUS))
        elif isinstance(node, QuestionNode):
            traverse(node.child)
            result.append(Token(T_QUESTION))
        else:
            raise ValueError("Nodo AST desconocido")
    traverse(ast)
    return result



def validarExpresion(expresion: str) -> bool:
    """
    Verifica paréntesis balanceados y operadores con operandos.
    Esto no es un parser completo, pero filtra errores básicos.
    """
    stack = []
    operadores_binarios = {'|', '.'}
    operadores_unarios = {'*','+','?'}
    todos = operadores_binarios.union(operadores_unarios)
    i = 0
    while i < len(expresion):
        c = expresion[i]
        if c == '(':
            stack.append(c)
            # Detectar "()"
            if i+1<len(expresion) and expresion[i+1] == ')':
                print(f"Error: Paréntesis vacío en {i} de '{expresion}'")
                return False
        elif c==')':
            if not stack:
                print(f"Error: ')' sin '(' previo en {i} de '{expresion}'")
                return False
            stack.pop()
        elif c=='|':
            # Checar si hay algo antes y después.
            # No lo hacemos super estricto, 
            pass
        elif c in operadores_binarios and c!='|':
            pass
        elif c in operadores_unarios:
            pass
        i+=1
    if stack:
        print(f"Error: Paréntesis sin cerrar en '{expresion}'")
        return False
    return True

############################
#   SHUNTING YARD 2.0
############################

# Tipos de token
T_CHAR     = 'CHAR'
T_LPAREN   = 'LPAREN'
T_RPAREN   = 'RPAREN'
T_UNION    = 'UNION'       # |
T_STAR     = 'STAR'        # *
T_PLUS     = 'PLUS'        # +
T_QUESTION = 'QUESTION'    # ?
T_CONCAT   = 'CONCAT'      # implícita
T_EOF      = 'EOF'

def get_token_precedence(ttype: str)->int:
    """
    Precedencia para tokens en shunting yard:
      UNION => 1
      CONCAT => 2
      STAR,PLUS,QUESTION => 3
    """
    if ttype==T_UNION:
        return 1
    elif ttype==T_CONCAT:
        return 2
    elif ttype in [T_STAR,T_PLUS,T_QUESTION]:
        return 3
    return 0

class Token:
    def __init__(self, ttype, val=None):
        self.type = ttype
        self.val  = val
    def __repr__(self):
        return f"Token({self.type},{self.val})"

def shuntingYard(regex: str) -> list:
    expanded = formatRegex(regex)
    tokens = tokenizeRegex(expanded)
    # NOTA: No llamamos a insertConcat, ya que el parser tratará la concatenación implícita.
    ast = parseRegex(tokens)
    postfix_tokens = astToPostfix(ast)
    print("AST:", ast)
    print("Postfix tokens:", postfix_tokens)
    return postfix_tokens



# Lista de símbolos válidos (ASCII 33 al 255)
VALID_ASCII = [chr(i) for i in range(33, 256)]

def tokenizeRegex(expr: str):
    """
    Convierte 'expr' en una lista de Tokens (T_CHAR, T_LPAREN, etc.).
    Maneja:
      - '(' , ')'
      - '|', '*', '+', '?'
      - escapes con '\'
      - corchetes [ ] => los convierte en T_CHAR con el contenido
      - literales entre comillas (simple o doble)
    """
    i = 0
    length = len(expr)
    result = []
    while i < length:
        c = expr[i]
        if c == '(':
            result.append(Token(T_LPAREN))
            i += 1
        elif c == ')':
            result.append(Token(T_RPAREN))
            i += 1
        elif c == '|':
            result.append(Token(T_UNION))
            i += 1
        elif c == '*':
            result.append(Token(T_STAR))
            i += 1
        elif c == '+':
            result.append(Token(T_PLUS))
            i += 1
        elif c == '?':
            result.append(Token(T_QUESTION))
            i += 1
        elif c == '[':
                # Expandimos el contenido del conjunto de caracteres como múltiples T_CHAR
            j = i + 1
            content = ''
            while j < length and expr[j] != ']':
                content += expr[j]
                j += 1
            i = j + 1  # Saltamos el ']'

            def expand_range(a, b):
                return [chr(c) for c in range(ord(a), ord(b) + 1)]

            def expand_class_inline(content):
                chars = []
                k = 0
                while k < len(content):
                    if content[k] == "'" and (k + 2 < len(content)) and content[k+2] == "'":
                        c1 = content[k+1]
                        k += 3
                        if k + 4 <= len(content) and content[k] == '-' and content[k+1] == "'" and content[k+3] == "'":
                            c2 = content[k+2]
                            chars.extend(expand_range(c1, c2))
                            k += 4
                        else:
                            chars.append(c1)
                    elif content[k] == '\\':
                        if k + 1 < len(content):
                            if content[k+1] == 't':
                                chars.append('\t')
                            elif content[k+1] == 'n':
                                chars.append('\n')
                            else:
                                chars.append(content[k+1])
                            k += 2
                        else:
                            chars.append('\\')
                            k += 1
                    elif content[k] == ' ':
                        chars.append(' ')
                        k += 1
                    else:
                        chars.append(content[k])
                        k += 1
                return chars

            class_chars = expand_class_inline(content)
            for ch in class_chars:
                result.append(Token(T_CHAR, ch))
                result.append(Token(T_UNION))
            if result and result[-1].type == T_UNION:
                result.pop()  # elimina el último '|'
        elif c in {"'", '"'}:
            # Si se encuentra una comilla, se recopila todo hasta la comilla de cierre
            quote = c
            j = i + 1
            literal = ""
            while j < length and expr[j] != quote:
                literal += expr[j]
                j += 1
            if j < length and expr[j] == quote:
                result.append(Token(T_CHAR, literal))
                i = j + 1
            else:
                # Si no se encuentra comilla de cierre, se añade el caracter y se continúa
                result.append(Token(T_CHAR, c))
                i += 1
        elif c == '\\' and i + 1 < length:
            escape_char = expr[i + 1]
            if escape_char == 'n':
                result.append(Token(T_CHAR, 'n'))
            elif escape_char == 't':
                result.append(Token(T_CHAR, 't'))
            elif escape_char in VALID_ASCII:
                result.append(Token(T_CHAR, escape_char))
            else:
                print(f"⚠️ Carácter escapado inválido: \\{escape_char}")
            i += 2
        else:
            # Un caracter normal
            result.append(Token(T_CHAR, c))
            i += 1
    result.append(Token(T_EOF))
    return result


def insertConcat(tokens: list):
    res = []
    prev = None
    # Consideramos que los siguientes tokens pueden funcionar como operandos:
    operandantes = {T_CHAR, T_RPAREN, T_STAR, T_PLUS, T_QUESTION}
    operanddespues = {T_CHAR, T_LPAREN}
    for tk in tokens:
        if prev:
            if prev.type in operandantes and tk.type in operanddespues:
                res.append(Token(T_CONCAT))
        res.append(tk)
        prev = tk
    return res


def applyShunt(tokens: list) -> list:
    output = []
    stack = []
    for tk in tokens:
        print("Procesando token:", tk, "Stack:", [s.type for s in stack], "Output:", [t.type for t in output])
        if tk.type == T_EOF:
            break
        if tk.type == T_CHAR:
            output.append(tk)  # agregamos el token tal como está
        elif tk.type == T_LPAREN:
            stack.append(tk)
        elif tk.type == T_RPAREN:
            while stack and stack[-1].type != T_LPAREN:
                output.append(stack.pop())
            if not stack:
                raise ValueError("Falta '(' en la expresión.")
            stack.pop()  # quita el T_LPAREN
        elif tk.type in [T_UNION, T_CONCAT, T_STAR, T_PLUS, T_QUESTION]:
            # Para operadores unarios (T_STAR, T_PLUS, T_QUESTION) usamos ">" en lugar de ">=".
            while stack and stack[-1].type != T_LPAREN and (
                (tk.type in [T_STAR, T_PLUS, T_QUESTION] and get_token_precedence(stack[-1].type) > get_token_precedence(tk.type))
                or (tk.type in [T_UNION, T_CONCAT] and get_token_precedence(stack[-1].type) >= get_token_precedence(tk.type))
            ):
                output.append(stack.pop())
            stack.append(tk)
        else:
            # ignoramos otros
            pass
    while stack:
        top = stack.pop()
        if top.type in [T_LPAREN, T_RPAREN]:
            raise ValueError("Paréntesis sin cerrar.")
        output.append(top)
    print("Final output tokens:", output)
    return output


def token2symbol(tk: Token)->str:
    if tk.type==T_UNION: return '|'
    elif tk.type==T_CONCAT: return '.'
    elif tk.type==T_STAR: return '*'
    elif tk.type==T_PLUS: return '+'
    elif tk.type==T_QUESTION: return '?'
    elif tk.type==T_CHAR: return tk.val 
    return ''

###########################
# formatRegex & helpers
###########################
def formatRegex(regex: str) -> str:
    # regexX = tranformClass(regex) ❌ Esto rompe el WHITESPACE
    regexX = tranformOpt(regex)
    regexX = considerPeriod(regexX)
    return regexX


def tranformOpt(string: str) -> str:
    # No transformamos el '?' aquí, lo manejaremos en el AFN.
    return string



def expand_range(start, end)->list:
    return [chr(i) for i in range(ord(start),ord(end)+1)]

def tranformClass(regex: str) -> str:
    output = ''
    i = 0
    while i < len(regex):
        if regex[i] == '[':
            i += 1
            expanded = []
            if i < len(regex) and regex[i] == '^':
                i += 1
                raise NotImplementedError("No soportamos ^negado todavía.")
            while i < len(regex) and regex[i] != ']':
                if (i + 6 < len(regex) and
                    regex[i] == "'" and regex[i+2] == "'" and 
                    regex[i+3] == '-' and regex[i+4] == "'" and 
                    regex[i+6] == "'"):
                    literal1 = regex[i+1]
                    literal2 = regex[i+5]
                    expanded += expand_range(literal1, literal2)
                    i += 7
                elif regex[i] == "'" and i+2 < len(regex) and regex[i+2] == "'":
                    char = regex[i+1]
                    if char == '\\':
                        if i+4 < len(regex) and regex[i+3] == '\\' and regex[i+4] == "'":
                            escape_seq = regex[i+2]
                            if escape_seq == 'n':
                                expanded.append('\n')
                            elif escape_seq == 't':
                                expanded.append('\t')
                            else:
                                expanded.append(escape_seq)
                            i += 5
                        else:
                            expanded.append('\\')
                            i += 3
                    else:
                        expanded.append(char)
                        i += 3
                else:
                    expanded.append(regex[i])
                    i += 1
            # Al final del while
            group = '|'.join(repr(c)[1:-1] if c in {' ', '\n', '\t'} else c for c in expanded)
            output += '(' + group + ')'
            if i < len(regex) and regex[i] == ']':
                i += 1
        else:
            output += regex[i]
            i += 1
    return output




def transformPosKleene(regex: str) -> str:
    # Si la expresión es de un solo carácter o es un literal escapado, no se transforma.
    if len(regex) <= 1 or (len(regex) == 2 and regex[0] == '\\'):
        return regex
    i = 0
    result = ""
    while i < len(regex):
        if regex[i] == '+':
            # Se requiere que haya un operando antes del '+'
            if not result:
                result += '+'
            else:
                if result[-1] == ')':
                    # Buscar la posición del paréntesis de apertura que empareja la última ')'
                    count = 0
                    j = len(result) - 1
                    while j >= 0:
                        if result[j] == ')':
                            count += 1
                        elif result[j] == '(':
                            count -= 1
                            if count == 0:
                                break
                        j -= 1
                    if j < 0:
                        result += '+'
                    else:
                        operand = result[j:]
                        result = result[:j] + operand + operand + '*'
                else:
                    # El operando es el último carácter
                    operand = result[-1]
                    result = result[:-1] + operand + operand + '*'
            i += 1
        else:
            result += regex[i]
            i += 1
    return result


def escapeChars(r: str)->str:
    """
    Escapa el slash si no va a ( ) { }.
    """
    out=''
    for i in range(len(r)):
        c=r[i]
        if i+1<len(r):
            if c=='\\' and r[i+1] not in ['(','}','{',')']:
                out+='\\'+c
            else:
                out+=c
        else:
            out+=c
    return out

def considerPeriod(r: str) -> str:
    """
    Reemplaza '.' por '\.' si no está escapado ya.
    """
    result = ''
    i = 0
    while i < len(r):
        if r[i] == '\\':
            # Preservar escape existente
            if i + 1 < len(r):
                result += r[i] + r[i+1]
                i += 2
            else:
                result += r[i]
                i += 1
        elif r[i] == '.':
            result += '\\.'
            i += 1
        else:
            result += r[i]
            i += 1
    return result


# --- AST para expresiones regulares ---

class RegexNode:
    pass

class LiteralNode(RegexNode):
    def __init__(self, value):
        self.value = value
    def __repr__(self):
        return f"Literal({self.value})"

class ConcatNode(RegexNode):
    def __init__(self, left, right):
        self.left = left
        self.right = right
    def __repr__(self):
        return f"Concat({self.left}, {self.right})"

class UnionNode(RegexNode):
    def __init__(self, left, right):
        self.left = left
        self.right = right
    def __repr__(self):
        return f"Union({self.left}, {self.right})"

class StarNode(RegexNode):
    def __init__(self, child):
        self.child = child
    def __repr__(self):
        return f"Star({self.child})"

class PlusNode(RegexNode):
    def __init__(self, child):
        self.child = child
    def __repr__(self):
        return f"Plus({self.child})"

class QuestionNode(RegexNode):
    def __init__(self, child):
        self.child = child
    def __repr__(self):
        return f"Question({self.child})"
