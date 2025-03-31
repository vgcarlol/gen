from utilidades import Stack

def leerArchivo():
    with open("input/expressions.txt", "r", encoding='utf-8') as archivo:
        lineas = archivo.readlines()
    
    expresiones_regulares = []

    for linea in lineas:
        linea = linea.strip()

        if not linea or linea.startswith("#"):
            # Ignora las líneas en blanco o comentarios
            continue

        # Validar la expresión
        if validarExpresion(linea):
            # Agrega la línea como una expresión regular
            expresiones_regulares.append(linea)
        else:
            print(f"Expresión inválida detectada y omitida: {linea}")

    return expresiones_regulares


def validarExpresion(expresion):
    stack = []
    operadores_binarios = {'|', '.'}
    operadores_unarios = {'*', '+', '?'}
    todos_operadores = operadores_binarios.union(operadores_unarios)
    indice = 0
    longitud = len(expresion)

    while indice < longitud:
        char = expresion[indice]

        if char == '(':
            stack.append(char)

            if indice + 1 < longitud and expresion[indice + 1] == ')':
                print(f"Error: Paréntesis vacío en posición {indice} en la expresión '{expresion}'")
                return False 
        elif char == ')':
            if not stack:
                print(f"Error: Paréntesis de cierre sin apertura en posición {indice} en la expresión '{expresion}'")
                return False 
            stack.pop()

        if char == '|':

            if indice == 0 or expresion[indice - 1] in todos_operadores or expresion[indice - 1] == '(':
                print(f"Error: Operador '|' sin operando izquierdo en posición {indice} en la expresión '{expresion}'")
                return False 
            if indice + 1 == longitud or expresion[indice + 1] in todos_operadores or expresion[indice + 1] == ')':
                print(f"Error: Operador '|' sin operando derecho en posición {indice} en la expresión '{expresion}'")
                return False  
            
        if char in operadores_binarios and char != '|':

            if indice == 0 or expresion[indice - 1] in todos_operadores or expresion[indice - 1] == '(':
                print(f"Error: Operador '{char}' sin operando izquierdo en posición {indice} en la expresión '{expresion}'")
                return False

            if indice + 1 == longitud or expresion[indice + 1] in todos_operadores or expresion[indice + 1] == ')':
                print(f"Error: Operador '{char}' sin operando derecho en posición {indice} en la expresión '{expresion}'")
                return False
            
        if char in operadores_unarios:
            if indice == 0 or expresion[indice - 1] in todos_operadores or expresion[indice - 1] == '(':
                print(f"Error: Operador '{char}' sin operando previo en posición {indice} en la expresión '{expresion}'")
                return False

        indice += 1

    if stack:
        print(f"Error: Paréntesis sin cerrar en la expresión '{expresion}'")
        return False 

    return True  


def getPrecedence(char):
    if char == '(':
        return 1
    elif char == '|':
        return 2
    elif char == '.':
        return 3
    elif char in ['?','*','+']:
        return 4
    elif char == '^':
        return 5
    else:
        return 6
 
def shuntingYard(regex: str):
    formatedRegex: str = formatRegex(regex)
    
    postfix: str = ''
    stack = Stack()
    escapeNextChar = False

    #Algoritmo de shunting yard con \ considerado
    for i in range(len(formatedRegex)):
        char1 = formatedRegex[i]
        
        if escapeNextChar:
            postfix += char1
            escapeNextChar = False
            continue

        if char1 == '\\':
            escapeNextChar = True
            continue

        if char1 == '(':
            stack.push(char1)
        elif char1 == ')':
            while stack.peek() != '(':
                postfix += stack.pop()
            stack.pop()
        else:
            while (not stack.isEmpty()):
                peekedchar = stack.peek()
                peekedCharPrecedence = getPrecedence(peekedchar)
                char1Precedence = getPrecedence(char1)
                if peekedCharPrecedence >= char1Precedence:
                    postfix += stack.pop()
                else:
                    break
            stack.push(char1)

    while (not stack.isEmpty()):
        postfix += stack.pop()                

    return postfix

def formatRegex(regex: str) -> str:
    allOperators = ['|', '?', '+', '*', '^']
    binaryOperators = ['|', '^']
    res = ''

    #Cada clase se convierte en secuencia de or's
    regexX = tranformClass(regex)

    #Transformar el caracter ?
    regexX = tranformOpt(regexX)

    #Tomar en cuenta el operador '+'
    regexX = transformPosKleene(regexX)

    #Escapar el caracter backslash y escapar su si
    regexX = escapeChars(regexX)

    #Tomar en cuenta el caracter 'punto'
    regexX = considerPeriod(regexX)

    #Formato: Agregar punto de concatenación
    escaped = False

    for i in range(len(regexX)):
        c1 = regexX[i]
        if i+1 < len(regexX):
            c2 = regexX[i+1]
            res += c1
            if c1 == '\\' and not escaped:
                escaped = True
                continue

            if (escaped) and (c2 != ')') and (c2 not in allOperators):
                res += '.'
                escaped = False
                continue

            if (c1 != '(') and (c2 != ')') and (c2 not in allOperators) and (c1 not in binaryOperators) and (c1 != '\\') and (not escaped):
                res += '.'    
            
    res += regexX[-1]
    return res

def tranformOpt(string):
    stack = []
    for char in string:
        if char != '?':
            stack.append(char)
        else:
            temp = ''
            if len(stack) > 0 and stack[-1] == ')':
                count = 1
                temp = stack.pop() + temp
                while count > 0:
                    if stack[-1] == ')':
                        count += 1
                    elif stack[-1] == '(':
                        count -= 1
                    temp = stack.pop() + temp
                temp = temp[1:-1]
            elif len(stack) > 0 and (stack[-1] not in '()*|'):
                while len(stack) > 0 and (stack[-1] not in '()*|'):
                    temp = stack.pop() + temp
            else:
                continue
            temp = r'(ε|' + temp + ')'
            stack.append(temp)
    return ''.join(stack)

def expand_range(start, end):
    return [chr(i) for i in range(ord(start), ord(end)+1)]

def tranformClass(regex):
    output = ''
    i = 0
    while i < len(regex):
        if regex[i] == '[':
            i += 1
            expanded = []
            negate = False

            if regex[i] == '^':
                negate = True
                i += 1

            while i < len(regex) and regex[i] != ']':
                if i+2 < len(regex) and regex[i+1] == '-':
                    expanded += expand_range(regex[i], regex[i+2])
                    i += 3
                else:
                    expanded.append(regex[i])
                    i += 1

            group = '|'.join(expanded)
            if negate:
                # Si implementas ^ más adelante
                raise NotImplementedError("Negación de clases aún no está soportada")
            output += f'({group})'
            i += 1
        else:
            output += regex[i]
            i += 1
    return output

def transformPosKleene(regex):
    output = ''
    balanceStack = Stack()
    stack = Stack()
    posKleene = False
    for i in range(len(regex)):
        char1 = regex[(len(regex)-1)-i]

        if char1 == '+':
            posKleene = True
            continue

        if posKleene == True:
            stack.push(char1)

            if char1 == ')':
                balanceStack.push(char1)
            elif char1 == '(':
                balanceStack.pop()

            if balanceStack.isEmpty():
                substring = '('
                while not stack.isEmpty():
                    substring += stack.pop()
                substring += substring + ')*' + ')'
                output = substring + output
                posKleene = False
        else:
            output = char1 + output

    return output

def escapeChars(regex):
    output = ''
    for i in range(len(regex)):
        char1 = regex[i]
        if i+1 < len(regex):
            if char1 == '\\' and regex[i+1] not in ['(',')','{','}']:
                output += '\\'
                output += char1
            else:
                output += char1
    output += regex[-1]

    return output


def considerPeriod(regex):
    result = ''
    for i in range(len(regex)):
        chara1 = regex[i]
        if i+1 < len(regex):
            if chara1 == '.':
                result += '\\'
                result += chara1
            else:
                result += chara1
    result += regex[-1]
    return result


