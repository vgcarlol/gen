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

def shuntingYard(regex: str) -> str:
    """
    Función principal que tu main.py llama.
    1) formatRegex => expandir clases, etc.
    2) tokenizeRegex => convertimos a tokens
    3) insertConcat => metemos CONCAT implícita
    4) applyShunt => generamos postfix
    """
    expanded = formatRegex(regex)
    tokens = tokenizeRegex(expanded)
    tokens2 = insertConcat(tokens)
    postfix = applyShunt(tokens2)
    return postfix

def tokenizeRegex(expr: str):
    """
    Convierte 'expr' en una lista de Tokens (T_CHAR, T_LPAREN, etc.).
    Maneja:
      - '(' , ')'
      - '|', '*', '+', '?'
      - escapes con '\'
      - corchetes [ ] => los convierte en T_CHAR con el contenido
    """
    i=0
    length=len(expr)
    result=[]
    while i<length:
        c=expr[i]
        if c.isspace():
            i+=1
            continue
        if c=='(':
            result.append(Token(T_LPAREN))
            i+=1
        elif c==')':
            result.append(Token(T_RPAREN))
            i+=1
        elif c=='|':
            result.append(Token(T_UNION))
            i+=1
        elif c=='*':
            result.append(Token(T_STAR))
            i+=1
        elif c=='+':
            result.append(Token(T_PLUS))
            i+=1
        elif c=='?':
            result.append(Token(T_QUESTION))
            i+=1
        elif c=='[':
            # Tomar todo hasta ']' y considerarlo un literal
            j=i+1
            bracketLevel=1
            content=''
            while j<length and bracketLevel>0:
                if expr[j]=='[':
                    bracketLevel+=1
                elif expr[j]==']':
                    bracketLevel-=1
                    if bracketLevel==0:
                        break
                content+=expr[j]
                j+=1
            # content es lo que hay dentro
            # lo ponemos como T_CHAR de todo ese bloque => p.e. [abc] => T_CHAR('[abc]')
            result.append(Token(T_CHAR,f'[{content}]'))
            i=j+1
        elif c=='\\' and i+1<length:
            # \x => T_CHAR(x)
            result.append(Token(T_CHAR, expr[i+1]))
            i+=2
        else:
            # un char normal
            result.append(Token(T_CHAR,c))
            i+=1
    result.append(Token(T_EOF))
    return result

def insertConcat(tokens: list):
    """
    Inserta T_CONCAT cuando dos tokens se pegan sin operador.
    Regla típica: 
      Si el token anterior es (CHAR,RPAREN) 
      y el siguiente es (CHAR,LPAREN), meto CONCAT
    """
    res=[]
    prev=None
    for tk in tokens:
        if prev:
            # Insertar CONCAT si prev es CHAR,RPAREN y tk es CHAR,LPAREN
            if prev.type in [T_CHAR,T_RPAREN] and tk.type in [T_CHAR,T_LPAREN]:
                res.append(Token(T_CONCAT))
        res.append(tk)
        prev=tk
    return res

def applyShunt(tokens: list)->str:
    """
    Aplica shunting yard a la lista de tokens => string postfix.
    """
    output=[]
    stack=[]
    for tk in tokens:
        if tk.type==T_EOF:
            break
        if tk.type==T_CHAR:
            # volcar su val al postfix
            output.append(tk.val)
        elif tk.type==T_LPAREN:
            stack.append(tk)
        elif tk.type==T_RPAREN:
            # desapilar
            while stack and stack[-1].type!=T_LPAREN:
                output.append( token2symbol(stack.pop()) )
            if not stack:
                raise ValueError("Falta '(' en la expresión.")
            stack.pop() # quita LPAREN
        elif tk.type in [T_UNION,T_CONCAT,T_STAR,T_PLUS,T_QUESTION]:
            while stack and stack[-1].type!=T_LPAREN and \
                  get_token_precedence(stack[-1].type)>=get_token_precedence(tk.type):
                output.append( token2symbol(stack.pop()) )
            stack.append(tk)
        else:
            # ignore
            pass
    while stack:
        top=stack.pop()
        if top.type in [T_LPAREN,T_RPAREN]:
            raise ValueError("Paréntesis sin cerrar.")
        output.append(token2symbol(top))
    return ''.join(output)

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
def formatRegex(regex: str)->str:
    """
    Conserva tu pipeline:
      1) tranformClass => [a-z] a (a|b|c...)
      2) tranformOpt => ? => (ε|x)
      3) transformPosKleene => x+ => xx*
      4) escapeChars => slash
      5) considerPeriod => '.' => '\.'
    y luego no insertamos '.' de concatenación, 
    porque lo manejamos en insertConcat.
    """
    regexX=tranformClass(regex)
    regexX=tranformOpt(regexX)
    regexX=transformPosKleene(regexX)
    regexX=escapeChars(regexX)
    regexX=considerPeriod(regexX)
    return regexX

def tranformOpt(string: str)->str:
    stack=[]
    for char in string:
        if char!='?':
            stack.append(char)
        else:
            temp=''
            if stack and stack[-1]==')':
                count=1
                temp=stack.pop()+temp
                while count>0 and stack:
                    top=stack.pop()
                    temp=top+temp
                    if top==')':
                        count+=1
                    elif top=='(':
                        count-=1
                temp=temp[1:-1]
            elif stack and (stack[-1] not in '()*|'):
                while stack and (stack[-1] not in '()*|'):
                    temp=stack.pop()+temp
            else:
                continue
            temp='(ε|'+temp+')'
            stack.append(temp)
    return ''.join(stack)

def expand_range(start, end)->list:
    return [chr(i) for i in range(ord(start),ord(end)+1)]

def tranformClass(regex: str)->str:
    """
    [a-z] => (a|b|...|z)
    [abc] => (a|b|c)
    """
    output=''
    i=0
    while i<len(regex):
        if regex[i]=='[':
            i+=1
            expanded=[]
            negate=False
            if i<len(regex) and regex[i]=='^':
                negate=True
                i+=1
                raise NotImplementedError("No soportamos ^negado todavia.")
            while i<len(regex) and regex[i]!=']':
                if (i+2<len(regex)) and regex[i+1]=='-':
                    expanded+=expand_range(regex[i],regex[i+2])
                    i+=3
                else:
                    expanded.append(regex[i])
                    i+=1
            # expanded = list de chars
            group='|'.join(expanded)
            output+='('+group+')'
            if i<len(regex) and regex[i]==']':
                i+=1
        else:
            output+=regex[i]
            i+=1
    return output

def transformPosKleene(regx: str)->str:
    """
    x+ => xx*
    (usa un stack invertido)
    """
    output=''
    stack=Stack()
    s2=Stack()
    posKleene=False
    for i in range(len(regx)):
        c=regx[(len(regx)-1)-i]
        if c=='+':
            posKleene=True
            continue
        if posKleene:
            stack.push(c)
            if c==')':
                s2.push(c)
            elif c=='(':
                s2.pop()
            if s2.isEmpty():
                # terminamos la subexp
                substring='('
                while not stack.isEmpty():
                    substring+=stack.pop()
                substring+=substring+')*'+')'
                output=substring+output
                posKleene=False
        else:
            output=c+output
    return output

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

def considerPeriod(r: str)->str:
    """
    Reemplaza '.' literal por '\.'
    """
    out=''
    for i in range(len(r)):
        c=r[i]
        if i+1<len(r) and c=='.':
            out+='\\.'
        else:
            out+=c
    return out
