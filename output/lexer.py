# AUTO-GENERADO: Analizador léxico basado en AFD

def analizar(texto):
    transitions = {
        ('A', 'd'): 'B',
        ('B', 'e'): 'C',
        ('C', 'l'): 'D',
        ('D', 'i'): 'E',
        ('E', 'm'): 'F',
        ('F', 'm'): 'G',
        ('G', 'm'): 'G',
    }

    accepting = {
        '9': 'WHITESPACE',
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
