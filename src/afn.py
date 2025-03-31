from utilidades import Stack

def character(c):
    start = 0
    accept = 1
    transitions = {(start, c): [accept]}
    return AFN(start, accept, transitions)

# Algoritmo de Thompson

def concatOperator(afn1, afn2):
    transitions = afn1.transitions.copy()

    for (state, symbol), next_states in afn2.transitions.items():
        if state != afn2.start:
            new_state = state + afn1.accept
        else:
            new_state = afn1.accept
        
        new_next_states = []
        for next_state in next_states:
            new_next_state = next_state + afn1.accept
            new_next_states.append(new_next_state)

        key = (new_state, symbol)
        transitions[key] = new_next_states

    return AFN(afn1.start, afn2.accept + afn1.accept, transitions)

def kleeneOperator(nfa):
    start = 0
    accept = nfa.accept + 2
    transitions = {(start, ''): [nfa.start + 1, accept], (nfa.accept + 1, ''): [nfa.start + 1, accept]}
    for (state, symbol), next_states in nfa.transitions.items():
        new_state = state + 1
        new_next_states = []
        for next_state in next_states:
            new_next_state = next_state + 1
            new_next_states.append(new_next_state)
        key = (new_state, symbol)
        transitions[key] = new_next_states

    return AFN(start, accept, transitions)

def orOperator(afn1, afn2):
    start = 0
    accept = afn1.accept + afn2.accept + 3
    transitions = {
        (start, ''): [afn1.start + 1, afn2.start + afn1.accept + 2],
        (afn1.accept + 1, ''): [accept],
        (afn2.accept + afn1.accept + 2, ''): [accept]
    }
    for (state, symbol), next_states in afn1.transitions.items():
        transitions[(state + 1, symbol)] = [next_state + 1 for next_state in next_states]
    for (state, symbol), next_states in afn2.transitions.items():
        transitions[(state + afn1.accept + 2, symbol)] = [next_state + afn1.accept + 2 for next_state in next_states]
    return AFN(start, accept, transitions)

def armarAFN(postfix):
    stack = Stack()
    
    for char in postfix:
        if char == '.':
            afn2 = stack.pop()
            afn1 = stack.pop()
            stack.push(concatOperator(afn1, afn2))
        elif char == '|':
            afn2 = stack.pop()
            afn1 = stack.pop()
            stack.push(orOperator(afn1, afn2))
        elif char == '*':
            nfa = stack.pop()
            stack.push(kleeneOperator(nfa))
        else:
            stack.push(character(char))
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

