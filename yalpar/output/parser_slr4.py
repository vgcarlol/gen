# AUTO-GENERADO: Parser SLR(1)

ACTION = \
{
    (0, 'ID'): ('shift', 1),
    (1, 'ASSIGNOP'): ('shift', 6),
    (2, '$'): ('reduce', 6),
    (2, 'SEMICOLON'): ('reduce', 6),
    (3, '$'): ('reduce', 1),
    (4, '$'): ('accept', None),
    (5, '$'): ('reduce', 3),
    (5, 'SEMICOLON'): ('shift', 8),
    (7, '$'): ('reduce', 2),
    (8, 'ID'): ('shift', 1),
    (9, '$'): ('reduce', 7),
    (9, 'SEMICOLON'): ('reduce', 7),
    (10, '$'): ('reduce', 9),
    (10, 'EQ'): ('shift', 19),
    (10, 'ID'): ('shift', 16),
    (10, 'LPAREN'): ('shift', 17),
    (10, 'LT'): ('shift', 12),
    (10, 'NUMBER'): ('shift', 15),
    (10, 'RPAREN'): ('reduce', 9),
    (10, 'SEMICOLON'): ('reduce', 9),
    (11, '$'): ('reduce', 5),
    (11, 'SEMICOLON'): ('shift', 8),
    (13, '$'): ('reduce', 12),
    (13, 'RPAREN'): ('reduce', 12),
    (13, 'SEMICOLON'): ('reduce', 12),
    (14, '$'): ('reduce', 18),
    (14, 'DIV'): ('shift', 24),
    (14, 'MINUS'): ('reduce', 18),
    (14, 'PLUS'): ('reduce', 18),
    (14, 'RPAREN'): ('reduce', 18),
    (14, 'SEMICOLON'): ('reduce', 18),
    (14, 'TIMES'): ('shift', 23),
    (15, '$'): ('reduce', 24),
    (15, 'DIV'): ('reduce', 24),
    (15, 'MINUS'): ('reduce', 24),
    (15, 'PLUS'): ('reduce', 24),
    (15, 'RPAREN'): ('reduce', 24),
    (15, 'SEMICOLON'): ('reduce', 24),
    (15, 'TIMES'): ('reduce', 24),
    (16, '$'): ('reduce', 25),
    (16, 'DIV'): ('reduce', 25),
    (16, 'MINUS'): ('reduce', 25),
    (16, 'PLUS'): ('reduce', 25),
    (16, 'RPAREN'): ('reduce', 25),
    (16, 'SEMICOLON'): ('reduce', 25),
    (16, 'TIMES'): ('reduce', 25),
    (18, '$'): ('reduce', 8),
    (18, 'RPAREN'): ('reduce', 8),
    (18, 'SEMICOLON'): ('reduce', 8),
    (20, '$'): ('reduce', 4),
    (21, '$'): ('reduce', 10),
    (21, 'RPAREN'): ('reduce', 10),
    (21, 'SEMICOLON'): ('reduce', 10),
    (22, '$'): ('reduce', 17),
    (22, 'MINUS'): ('reduce', 17),
    (22, 'PLUS'): ('reduce', 17),
    (22, 'RPAREN'): ('reduce', 17),
    (22, 'SEMICOLON'): ('reduce', 17),
    (23, 'ID'): ('shift', 16),
    (23, 'LPAREN'): ('shift', 17),
    (23, 'NUMBER'): ('shift', 15),
    (24, 'ID'): ('shift', 16),
    (24, 'LPAREN'): ('shift', 17),
    (24, 'NUMBER'): ('shift', 15),
    (25, '$'): ('reduce', 20),
    (25, 'DIV'): ('shift', 24),
    (25, 'MINUS'): ('reduce', 20),
    (25, 'PLUS'): ('reduce', 20),
    (25, 'RPAREN'): ('reduce', 20),
    (25, 'SEMICOLON'): ('reduce', 20),
    (25, 'TIMES'): ('shift', 23),
    (26, 'RPAREN'): ('shift', 31),
    (28, '$'): ('reduce', 21),
    (28, 'DIV'): ('reduce', 21),
    (28, 'MINUS'): ('reduce', 21),
    (28, 'PLUS'): ('reduce', 21),
    (28, 'RPAREN'): ('reduce', 21),
    (28, 'SEMICOLON'): ('reduce', 21),
    (28, 'TIMES'): ('reduce', 21),
    (29, '$'): ('reduce', 22),
    (29, 'DIV'): ('reduce', 22),
    (29, 'MINUS'): ('reduce', 22),
    (29, 'PLUS'): ('reduce', 22),
    (29, 'RPAREN'): ('reduce', 22),
    (29, 'SEMICOLON'): ('reduce', 22),
    (29, 'TIMES'): ('reduce', 22),
    (30, '$'): ('reduce', 19),
    (30, 'MINUS'): ('reduce', 19),
    (30, 'PLUS'): ('reduce', 19),
    (30, 'RPAREN'): ('reduce', 19),
    (30, 'SEMICOLON'): ('reduce', 19),
    (31, '$'): ('reduce', 23),
    (31, 'DIV'): ('reduce', 23),
    (31, 'MINUS'): ('reduce', 23),
    (31, 'PLUS'): ('reduce', 23),
    (31, 'RPAREN'): ('reduce', 23),
    (31, 'SEMICOLON'): ('reduce', 23),
    (31, 'TIMES'): ('reduce', 23),
    (32, 'ID'): ('shift', 16),
    (32, 'LPAREN'): ('shift', 17),
    (32, 'NUMBER'): ('shift', 15),
    (33, 'MINUS'): ('shift', 34),
    (33, 'PLUS'): ('shift', 36),
    (34, 'ID'): ('shift', 16),
    (34, 'LPAREN'): ('shift', 17),
    (34, 'NUMBER'): ('shift', 15),
    (35, '$'): ('reduce', 11),
    (35, 'RPAREN'): ('reduce', 11),
    (35, 'SEMICOLON'): ('reduce', 11),
    (36, 'ID'): ('shift', 16),
    (36, 'LPAREN'): ('shift', 17),
    (36, 'NUMBER'): ('shift', 15),
    (37, '$'): ('reduce', 14),
    (37, 'MINUS'): ('shift', 34),
    (37, 'PLUS'): ('shift', 36),
    (37, 'RPAREN'): ('reduce', 14),
    (37, 'SEMICOLON'): ('reduce', 14),
    (38, '$'): ('reduce', 16),
    (38, 'MINUS'): ('reduce', 16),
    (38, 'PLUS'): ('reduce', 16),
    (38, 'RPAREN'): ('reduce', 16),
    (38, 'SEMICOLON'): ('reduce', 16),
    (39, '$'): ('reduce', 15),
    (39, 'MINUS'): ('reduce', 15),
    (39, 'PLUS'): ('reduce', 15),
    (39, 'RPAREN'): ('reduce', 15),
    (39, 'SEMICOLON'): ('reduce', 15),
    (40, '$'): ('reduce', 13),
    (40, 'RPAREN'): ('reduce', 13),
    (40, 'SEMICOLON'): ('reduce', 13),
}

GOTO = \
{
    (0, 'a'): 2,
    (0, 'm'): 5,
    (0, 'p'): 4,
    (0, 't'): 3,
    (5, 'q'): 7,
    (6, 'e'): 9,
    (6, 'x'): 10,
    (8, 'a'): 2,
    (8, 'm'): 11,
    (10, 'f'): 14,
    (10, 'r'): 13,
    (10, 'z'): 18,
    (11, 'q'): 20,
    (12, 'x'): 21,
    (14, 'j'): 25,
    (14, 'v'): 22,
    (17, 'e'): 26,
    (17, 'x'): 10,
    (19, 'x'): 27,
    (23, 'f'): 28,
    (24, 'f'): 29,
    (25, 'j'): 25,
    (25, 'v'): 30,
    (27, 'x:'): 32,
    (32, 'f'): 14,
    (32, 'r'): 33,
    (33, 'w'): 35,
    (33, 'y'): 37,
    (34, 'f'): 14,
    (34, 'r'): 38,
    (36, 'f'): 14,
    (36, 'r'): 39,
    (37, 'w'): 40,
    (37, 'y'): 37,
}

productions = [
    ("p'", ['p']),
    ('p', ['t']),
    ('t', ['m', 'q']),
    ('t', ['m']),
    ('q', ['SEMICOLON', 'm', 'q']),
    ('q', ['SEMICOLON', 'm']),
    ('m', ['a']),
    ('a', ['ID', 'ASSIGNOP', 'e']),
    ('e', ['x', 'z']),
    ('e', ['x']),
    ('z', ['LT', 'x']),
    ('z', ['EQ', 'x', 'x:', 'r', 'w']),
    ('z', ['r']),
    ('w', ['y', 'w']),
    ('w', ['y']),
    ('y', ['PLUS', 'r']),
    ('y', ['MINUS', 'r']),
    ('r', ['f', 'v']),
    ('r', ['f']),
    ('v', ['j', 'v']),
    ('v', ['j']),
    ('j', ['TIMES', 'f']),
    ('j', ['DIV', 'f']),
    ('f', ['LPAREN', 'e', 'RPAREN']),
    ('f', ['NUMBER']),
    ('f', ['ID']),
]

augmented_start = "p'"


def parse(tokens):
    """
    tokens: lista de tuplas (lexema, token), e.g. [('id','ID'), ('+','PLUS'), ..., ('$','$')]
    Simula el parser SLR(1), imprimiendo cada paso (SHIFT, REDUCE, GOTO, ACCEPT).
    Si hay error, lo notifica y devuelve False. Si acepta, devuelve True.
    """
    stack_states = [0]
    stack_symbols = []
    i = 0

    while True:
        estado = stack_states[-1]
        if i >= len(tokens):
            print("Error: no hay más tokens, falta '$'")
            return False
        lexema, tok = tokens[i]
        key = (estado, tok)
        if key not in ACTION:
            print(f"Error sintáctico: estado={estado}, token '{tok}' no esperado.")
            return False
        act = ACTION[key]
        if act[0] == 'shift':
            j = act[1]
            stack_states.append(j)
            stack_symbols.append((lexema, tok))
            print(f"SHIFT: estado={estado} --token '{tok}'--> push estado {j}, símbolo ('{lexema}','{tok}')")
            i += 1
        elif act[0] == 'reduce':
            prod_idx = act[1]
            lhs, rhs = productions[prod_idx]
            # Desapilar |rhs| elementos
            for _ in rhs:
                stack_states.pop()
                stack_symbols.pop()
            print(f"REDUCE: usar producción {prod_idx}: {lhs} → {' '.join(rhs)}")
            estado_prev = stack_states[-1]
            goto_key = (estado_prev, lhs)
            if goto_key not in GOTO:
                print(f"Error GOTO: no hay GOTO[{estado_prev}, {lhs}]")
                return False
            new_state = GOTO[goto_key]
            stack_states.append(new_state)
            stack_symbols.append((lhs, 'NT'))
            print(f"GOTO: estado={estado_prev} con no-term '{lhs}' → push estado {new_state}")
        elif act[0] == 'accept':
            print("ACCEPT: cadena sintácticamente correcta.")
            return True
        else:
            print("Acción desconocida en la tabla ACTION.")
            return False
