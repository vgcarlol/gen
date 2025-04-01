# Código: afn.py
from utilidades import Stack

def character(c):
    start = 0
    accept = 1
    transitions = {(start, c): [accept]}
    return AFN(start, accept, transitions)

# Algoritmo de Thompson

def concatOperator(afn1, afn2):
    # Calculamos el offset: número total de estados en afn1
    offset = afn1.accept + 1
    transitions = afn1.transitions.copy()

    # Reindexamos las transiciones de afn2
    for (state, symbol), next_states in afn2.transitions.items():
        # Si el estado es el inicial de afn2, se fusiona con el estado de aceptación de afn1
        if state == afn2.start:
            new_state = afn1.accept
        else:
            new_state = state + offset

        new_next_states = []
        for next_state in next_states:
            # De igual forma, el estado inicial de afn2 se fusiona
            if next_state == afn2.start:
                new_next_state = afn1.accept
            else:
                new_next_state = next_state + offset
            new_next_states.append(new_next_state)

        transitions[(new_state, symbol)] = new_next_states

    # El nuevo estado de aceptación es el de afn2, reindexado (no se fusiona)
    new_accept = afn2.accept + offset
    return AFN(afn1.start, new_accept, transitions)


def kleeneOperator(nfa):
    # Se crea un nuevo estado de inicio y uno de aceptación
    new_start = 0
    # Se desplaza todo el AFN interno en 1 posición
    offset = 1
    new_accept = nfa.accept + offset + 1  # nfa.accept + 2

    transitions = {
        (new_start, ''): [nfa.start + offset, new_accept],
        (nfa.accept + offset, ''): [nfa.start + offset, new_accept]
    }
    for (state, symbol), next_states in nfa.transitions.items():
        new_state = state + offset
        new_next_states = [ns + offset for ns in next_states]
        transitions[(new_state, symbol)] = new_next_states

    return AFN(new_start, new_accept, transitions)


def orOperator(afn1, afn2):
    # Nuevo estado de inicio y nuevo estado de aceptación
    new_start = 0
    offset = afn1.accept + 1  # desplazamiento para afn1
    offset2 = offset + (afn2.accept + 1)  # desplazamiento para afn2

    new_accept = offset2  # el último estado será el de aceptación final

    transitions = {
        (new_start, ''): [afn1.start + 1, afn2.start + offset],
        (afn1.accept + 1, ''): [new_accept],
        (afn2.accept + offset, ''): [new_accept]
    }
    # Reindexamos afn1: se le suma 1
    for (state, symbol), next_states in afn1.transitions.items():
        transitions[(state + 1, symbol)] = [ns + 1 for ns in next_states]
    # Reindexamos afn2: se le suma el offset calculado
    for (state, symbol), next_states in afn2.transitions.items():
        transitions[(state + offset, symbol)] = [ns + offset for ns in next_states]

    return AFN(new_start, new_accept, transitions)


def epsilonOperator():
    # Crea un AFN que reconoce la cadena vacía
    start = 0
    accept = 1
    transitions = {(start, ''): [accept]}
    return AFN(start, accept, transitions)

from regex_functions import T_CHAR, T_CONCAT, T_UNION, T_STAR, T_PLUS, T_QUESTION

def armarAFN(postfix_tokens):
    stack = Stack()
    for token in postfix_tokens:
        if token.type == T_CONCAT:
            afn2 = stack.pop()
            afn1 = stack.pop()
            stack.push(concatOperator(afn1, afn2))
        elif token.type == T_UNION:
            afn2 = stack.pop()
            afn1 = stack.pop()
            stack.push(orOperator(afn1, afn2))
        elif token.type == T_STAR:
            nfa = stack.pop()
            stack.push(kleeneOperator(nfa))
        elif token.type == T_PLUS:
            nfa = stack.pop()
            stack.push(concatOperator(nfa, kleeneOperator(nfa)))
        elif token.type == T_QUESTION:
            nfa = stack.pop()
            eps = epsilonOperator()
            stack.push(orOperator(eps, nfa))
        elif token.type == T_CHAR:
            stack.push(character(token.val))
        else:
            raise ValueError(f"Token inesperado: {token}")
    if stack.size() != 1:
        raise ValueError("La notación postfix generó un número incorrecto de operandos.")
    return stack.pop()



class AFN:
    def __init__(self, start, accept, transitions):
        self.start = start
        self.accept = accept
        self.transitions = transitions

    def getTransitions(self):
        return self.transitions
    def getStart(self):
        return self.start
    def getAccept(self):
        return self.accept

