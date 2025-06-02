# AUTO-GENERADO: Parser SLR(1)

ACTION = \
{
    (0, 'ID'): ('shift', 6),
    (0, 'LPAREN'): ('shift', 2),
    (0, 'NUMBER'): ('shift', 3),
    (1, '$'): ('accept', None),
    (2, 'ID'): ('shift', 6),
    (2, 'LPAREN'): ('shift', 2),
    (2, 'NUMBER'): ('shift', 3),
    (3, 'DIV'): ('reduce', 13),
    (3, 'MINUS'): ('reduce', 13),
    (3, 'PLUS'): ('reduce', 13),
    (3, 'RPAREN'): ('reduce', 13),
    (3, 'SEMICOLON'): ('reduce', 13),
    (3, 'TIMES'): ('reduce', 13),
    (4, '$'): ('reduce', 2),
    (4, 'SEMICOLON'): ('reduce', 2),
    (5, 'DIV'): ('reduce', 10),
    (5, 'MINUS'): ('reduce', 10),
    (5, 'PLUS'): ('reduce', 10),
    (5, 'RPAREN'): ('reduce', 10),
    (5, 'SEMICOLON'): ('reduce', 10),
    (5, 'TIMES'): ('reduce', 10),
    (6, 'DIV'): ('reduce', 12),
    (6, 'MINUS'): ('reduce', 12),
    (6, 'PLUS'): ('reduce', 12),
    (6, 'RPAREN'): ('reduce', 12),
    (6, 'SEMICOLON'): ('reduce', 12),
    (6, 'TIMES'): ('reduce', 12),
    (7, 'DIV'): ('shift', 11),
    (7, 'MINUS'): ('reduce', 7),
    (7, 'PLUS'): ('reduce', 7),
    (7, 'RPAREN'): ('reduce', 7),
    (7, 'SEMICOLON'): ('reduce', 7),
    (7, 'TIMES'): ('shift', 12),
    (8, 'MINUS'): ('shift', 14),
    (8, 'PLUS'): ('shift', 15),
    (8, 'SEMICOLON'): ('shift', 13),
    (9, '$'): ('reduce', 1),
    (9, 'SEMICOLON'): ('shift', 16),
    (10, 'MINUS'): ('shift', 14),
    (10, 'PLUS'): ('shift', 15),
    (10, 'RPAREN'): ('shift', 17),
    (11, 'ID'): ('shift', 6),
    (11, 'LPAREN'): ('shift', 2),
    (11, 'NUMBER'): ('shift', 3),
    (12, 'ID'): ('shift', 6),
    (12, 'LPAREN'): ('shift', 2),
    (12, 'NUMBER'): ('shift', 3),
    (13, '$'): ('reduce', 4),
    (13, 'SEMICOLON'): ('reduce', 4),
    (14, 'ID'): ('shift', 6),
    (14, 'LPAREN'): ('shift', 2),
    (14, 'NUMBER'): ('shift', 3),
    (15, 'ID'): ('shift', 6),
    (15, 'LPAREN'): ('shift', 2),
    (15, 'NUMBER'): ('shift', 3),
    (16, 'ID'): ('shift', 6),
    (16, 'LPAREN'): ('shift', 2),
    (16, 'NUMBER'): ('shift', 3),
    (17, 'DIV'): ('reduce', 11),
    (17, 'MINUS'): ('reduce', 11),
    (17, 'PLUS'): ('reduce', 11),
    (17, 'RPAREN'): ('reduce', 11),
    (17, 'SEMICOLON'): ('reduce', 11),
    (17, 'TIMES'): ('reduce', 11),
    (18, 'DIV'): ('reduce', 9),
    (18, 'MINUS'): ('reduce', 9),
    (18, 'PLUS'): ('reduce', 9),
    (18, 'RPAREN'): ('reduce', 9),
    (18, 'SEMICOLON'): ('reduce', 9),
    (18, 'TIMES'): ('reduce', 9),
    (19, 'DIV'): ('reduce', 8),
    (19, 'MINUS'): ('reduce', 8),
    (19, 'PLUS'): ('reduce', 8),
    (19, 'RPAREN'): ('reduce', 8),
    (19, 'SEMICOLON'): ('reduce', 8),
    (19, 'TIMES'): ('reduce', 8),
    (20, 'DIV'): ('shift', 11),
    (20, 'MINUS'): ('reduce', 6),
    (20, 'PLUS'): ('reduce', 6),
    (20, 'RPAREN'): ('reduce', 6),
    (20, 'SEMICOLON'): ('reduce', 6),
    (20, 'TIMES'): ('shift', 12),
    (21, 'DIV'): ('shift', 11),
    (21, 'MINUS'): ('reduce', 5),
    (21, 'PLUS'): ('reduce', 5),
    (21, 'RPAREN'): ('reduce', 5),
    (21, 'SEMICOLON'): ('reduce', 5),
    (21, 'TIMES'): ('shift', 12),
    (22, '$'): ('reduce', 3),
    (22, 'SEMICOLON'): ('reduce', 3),
}

GOTO = \
{
    (0, 'expression'): 8,
    (0, 'factor'): 5,
    (0, 'program'): 1,
    (0, 'statement'): 4,
    (0, 'statement_list'): 9,
    (0, 'term'): 7,
    (2, 'expression'): 10,
    (2, 'factor'): 5,
    (2, 'term'): 7,
    (11, 'factor'): 18,
    (12, 'factor'): 19,
    (14, 'factor'): 5,
    (14, 'term'): 20,
    (15, 'factor'): 5,
    (15, 'term'): 21,
    (16, 'expression'): 8,
    (16, 'factor'): 5,
    (16, 'statement'): 22,
    (16, 'term'): 7,
}

productions = [
    ("program'", ['program']),
    ('program', ['statement_list']),
    ('statement_list', ['statement']),
    ('statement_list', ['statement_list', 'SEMICOLON', 'statement']),
    ('statement', ['expression', 'SEMICOLON']),
    ('expression', ['expression', 'PLUS', 'term']),
    ('expression', ['expression', 'MINUS', 'term']),
    ('expression', ['term']),
    ('term', ['term', 'TIMES', 'factor']),
    ('term', ['term', 'DIV', 'factor']),
    ('term', ['factor']),
    ('factor', ['LPAREN', 'expression', 'RPAREN']),
    ('factor', ['ID']),
    ('factor', ['NUMBER']),
]

augmented_start = "program'"


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
