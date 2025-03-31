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
    tokens2 = insertConcat(tokens)
    postfix_tokens = applyShunt(tokens2)
        
    print("Tokens:", tokens2)
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
            # Tomar todo hasta ']' y considerarlo un literal
            j = i + 1
            bracketLevel = 1
            content = ''
            while j < length and bracketLevel > 0:
                if expr[j] == '[':
                    bracketLevel += 1
                elif expr[j] == ']':
                    bracketLevel -= 1
                    if bracketLevel == 0:
                        break
                content += expr[j]
                j += 1
            # content es lo que hay dentro de los corchetes
            result.append(Token(T_CHAR, f'[{content}]'))
            i = j + 1
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
                result.append(Token(T_CHAR, '\n'))
            elif escape_char == 't':
                result.append(Token(T_CHAR, '\t'))
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
    regexX = tranformClass(regex)
    regexX = tranformOpt(regexX)
    # Se omite la transformación de '+' para que se procese directamente en armarAFN
    # regexX = transformPosKleene(regexX)
    regexX = considerPeriod(regexX)
    return regexX


def tranformOpt(string: str) -> str:
    # No transformamos el '?' aquí, lo manejaremos en el AFN.
    return string



def expand_range(start, end)->list:
    return [chr(i) for i in range(ord(start),ord(end)+1)]

def tranformClass(regex: str) -> str:
    """
    Transforma expresiones entre corchetes.
    Ejemplo: ['A'-'Z''a'-'z'] -> ((A|B|...|Z)|(a|b|...|z))
    """
    output = ''
    i = 0
    while i < len(regex):
        if regex[i] == '[':
            i += 1
            expanded = []
            # Si aparece un '^', no lo soportamos (como indica tu código)
            if i < len(regex) and regex[i] == '^':
                i += 1
                raise NotImplementedError("No soportamos ^negado todavía.")
            while i < len(regex) and regex[i] != ']':
                # Detecta rango escrito como: 'X'-'Y'
                if (i + 6 < len(regex) and
                    regex[i] == "'" and regex[i+2] == "'" and 
                    regex[i+3] == '-' and regex[i+4] == "'" and 
                    regex[i+6] == "'"):
                    start = regex[i+1]
                    end = regex[i+5]
                    expanded += expand_range(start, end)
                    i += 7
                else:
                    expanded.append(regex[i])
                    i += 1
            group = '|'.join(expanded)
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
    out = ''
    for c in r:
        if c == '.':
            out += r'\.'  # Se agrega la barra y el punto
        else:
            out += c
    return out
