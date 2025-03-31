# AUTO-GENERADO: Analizador léxico basado en AFD

def analizar(texto):
    transitions = {
        ('A', ';'): 'B',
        ('A', '<'): 'C',
        ('A', ')'): 'D',
        ('A', 'n'): 'E',
        ('A', '-'): 'F',
        ('A', '9'): 'G',
        ('A', ':'): 'H',
        ('A', '\\'): 'I',
        ('A', "'"): 'J',
        ('A', '='): 'K',
        ('A', 't'): 'L',
        ('A', '('): 'M',
        ('A', '/'): 'N',
        ('E', '\\'): 'O',
        ('G', ')'): 'P',
        ('H', '='): 'Q',
        ('I', ')'): 'R',
        ('I', '\\'): 'S',
        ('J', ')'): 'T',
        ('J', '\\'): 'U',
        ('L', '\\'): 'V',
        ('M', ')'): 'W',
        ('M', '('): 'X',
        ('P', ')'): 'Y',
        ('R', ')'): 'R',
        ('S', '\\'): 'Z',
        ('T', ')'): '[',
        ('W', ')'): 'W',
        ('X', '('): '\\',
        ('Y', ')'): ']',
        ('Z', '\\'): 'Z',
        ('[', '('): '^',
        ('\\', '\\'): '_',
        ('^', ')'): '`',
        ('`', ')'): '`',
    }

    accepting = {
        51: 'WHITESPACE',
        64: 'ID',
        67: 'SEMICOLON',
        71: 'ASSIGNOP',
        74: 'LT',
        77: 'EQ',
        83: 'PLUS',
        86: 'MINUS',
        91: 'TIMES',
        94: 'DIV',
        97: 'LPAREN',
        100: 'RPAREN',
    }


    estado_actual = 'A'
    lexema = ''
    tokens = []
    i = 0

    while i < len(texto):
        c = texto[i]
        if (estado_actual, c) in transitions:
            estado_actual = transitions[(estado_actual, c)]
            lexema += c
            i += 1
        else:
            if estado_actual in accepting:
                tokens.append((lexema, accepting[estado_actual]))
                estado_actual = 'A'
                lexema = ''
            elif lexema:
                tokens.append((lexema, 'ERROR'))
                estado_actual = 'A'
                lexema = ''
            else:
                tokens.append((c, 'ERROR'))
                i += 1

    if lexema:
        if estado_actual in accepting:
            tokens.append((lexema, accepting[estado_actual]))
        else:
            tokens.append((lexema, 'ERROR'))

    return tokens

if __name__ == '__main__':
    with open('input/codigo.txt', 'r', encoding='utf-8') as file:
        contenido = file.read()
        resultado = analizar(contenido)
        for lexema, token in resultado:
            print(f"{lexema} -> {token}")
