# AUTO-GENERADO: Analizador léxico basado en AFD

def analizar(texto):
    transitions = {
        ('A', '('): 'B',
        ('A', ';'): 'C',
        ('A', '\\'): 'D',
        ('A', '9'): 'E',
        ('A', '='): 'F',
        ('A', 'n'): 'G',
        ('A', ')'): 'H',
        ('A', '/'): 'I',
        ('A', 't'): 'J',
        ('A', '-'): 'K',
        ('A', ':'): 'L',
        ('A', "'"): 'M',
        ('A', '<'): 'N',
        ('B', '('): 'O',
        ('B', ')'): 'P',
        ('D', '\\'): 'Q',
        ('D', ')'): 'R',
        ('E', ')'): 'S',
        ('G', '\\'): 'T',
        ('J', '\\'): 'U',
        ('L', '='): 'V',
        ('M', '\\'): 'W',
        ('M', ')'): 'X',
        ('O', '('): 'Y',
        ('P', ')'): 'P',
        ('Q', '\\'): 'Z',
        ('R', ')'): 'R',
        ('S', ')'): '[',
        ('X', ')'): '\\',
        ('Y', '\\'): ']',
        ('Z', '\\'): 'Z',
        ('[', ')'): '^',
        ('\\', '('): '_',
        ('_', ')'): '`',
        ('`', ')'): '`',
    }

    accepting = {
        'A': 'TIMES',
        'B': 'PLUS',
        'C': 'SEMICOLON',
        'D': 'ID',
        'F': 'EQ',
        'H': 'RPAREN',
        'I': 'DIV',
        'K': 'MINUS',
        'N': 'LT',
        'P': 'PLUS',
        'Q': 'WHITESPACE',
        'R': 'ID',
        'T': 'WHITESPACE',
        'U': 'WHITESPACE',
        'V': 'ASSIGNOP',
        'W': 'WHITESPACE',
        'Z': 'TIMES',
        ']': 'WHITESPACE',
        '^': 'ID',
        '`': 'WHITESPACE',
    }


    estado_inicial = 'A'
    tokens = []
    i = 0
    while i < len(texto):
        estado_actual = estado_inicial
        lexema = ''
        ultimo_token = None
        ultimo_index = i

        j = i
        while j < len(texto):
            c = texto[j]
            if (estado_actual, c) in transitions:
                estado_actual = transitions[(estado_actual, c)]
                lexema += c
                if estado_actual in accepting:
                    ultimo_token = (lexema, accepting[estado_actual])
                    ultimo_index = j + 1
                j += 1
            else:
                break

        if ultimo_token:
            tokens.append(ultimo_token)
            i = ultimo_index
        else:
            tokens.append((texto[i], 'ERROR'))
            i += 1

    return tokens

if __name__ == '__main__':
    with open('input/random_data_3.txt', 'r', encoding='utf-8') as file:
        contenido = file.read()
        resultado = analizar(contenido)

    with open('output/tokens.txt', 'w', encoding='utf-8') as out:
        for lexema, token in resultado:
            out.write(f"{lexema} -> {token}\n")
