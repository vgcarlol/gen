# Código: afd.py
import copy 
import string
from utilidades import conjuntoToString  # Para la conversión de conjuntos a cadenas
from graphviz import Digraph


# Subconjuntos
def formarSubconjunto(conjuntoActual, transitions):
    nuevoConjunto = set(conjuntoActual) 

    for i in conjuntoActual:
        for j in transitions.keys():
            if j[0] == i and j[1] == '': 
                for k in transitions[(i, j[1])]:
                    nuevoConjunto.add(k)

    if nuevoConjunto != set(conjuntoActual):
        return formarSubconjunto(nuevoConjunto, transitions)
    else:
        return nuevoConjunto

def epsilon_closure(states, transitions):
    stack = list(states)
    closure = set(states)

    while stack:
        state = stack.pop()
        for (src, symbol), dests in transitions.items():
            if src == state and symbol == '':
                for dest in dests:
                    if dest not in closure:
                        closure.add(dest)
                        stack.append(dest)
    return closure

def move(states, symbol, transitions):
    result = set()
    for state in states:
        if (state, symbol) in transitions:
            result.update(transitions[(state, symbol)])
    return result

def subconjuntos(afn):
    afn_transitions = afn.getTransitions()
    alphabet = set(symbol for (_, symbol) in afn_transitions if symbol != '')
    
    # Mapear transiciones ε con ''
    transitions = {}
    for (state, symbol), dests in afn_transitions.items():
        transitions[(state, '' if symbol == 'ε' else symbol)] = dests

    start_closure = epsilon_closure({afn.getStart()}, transitions)
    dfa_states = [start_closure]
    dfa_state_names = {frozenset(start_closure): 'A'}
    dfa_transitions = {}
    state_queue = [start_closure]
    next_state_id = ord('B')

    while state_queue:
        current = state_queue.pop(0)
        current_name = dfa_state_names[frozenset(current)]

        for symbol in alphabet:
            move_result = move(current, symbol, transitions)
            closure = epsilon_closure(move_result, transitions)

            if not closure:
                continue

            closure_frozen = frozenset(closure)
            if closure_frozen not in dfa_state_names:
                dfa_state_names[closure_frozen] = chr(next_state_id)
                state_queue.append(closure)
                next_state_id += 1

            to_state = dfa_state_names[closure_frozen]
            dfa_transitions[(current_name, symbol)] = to_state

    # Estados de aceptación
    accepting_states = []
    for closure_set, name in dfa_state_names.items():
        if afn.getAccept() in closure_set:
            accepting_states.append(name)

    start_state = dfa_state_names[frozenset(start_closure)]

    return AFD(start_state, accepting_states, dfa_transitions)


# Minimización
def minimizacion(afd):
    afdTransitions = afd.getTransitions() # Transiciones del AFD
    afdStart = afd.getStart() # Estado inicial del AFD
    afdAccept = afd.getAccept() # Estados de aceptación del AFD

    pi_0 = []
    non_accepting_states = [state for state, _ in afdTransitions.keys() if state not in afd.getAccept()]
    pi_0.append(non_accepting_states)   
    pi_0.append(afd.getAccept())

    allchars = sorted(list(set([char for _, char in afdTransitions.keys()])))

    while True:
        new_partitions = []
        
        for subset in pi_0:
            partitions = {} 

            for state in subset:
                key = tuple() 
                for char in allchars:
                    if (state, char) in afdTransitions:
                        destination = afdTransitions[(state, char)]
                        for index, category in enumerate(pi_0):
                            if destination in category:
                                key += (index,)
                                break
                    else:
                        key += (-1,) 

                if key not in partitions:
                    partitions[key] = []
                partitions[key].append(state)

            new_partitions.extend(partitions.values())

        if len(new_partitions) == len(pi_0): # Si no hubo cambios en las particiones entonces terminar
            break
        pi_0 = new_partitions

    new_partitions2 = []
    for i in pi_0:
        temp = []
        for j in i:
            if j not in temp:
                temp.append(j)

        if len(temp) > 0:
            new_partitions2.append(temp)

    pi_0 = new_partitions2

    simplified_transitions = {} # Construccion del AFD minimizado
    for char in allchars:
        for subset in pi_0:
            source_state = ','.join(subset)
            if (subset[0], char) in afdTransitions: 
                destination = afdTransitions[(subset[0], char)]
                for category in pi_0:
                    if destination in category:
                        simplified_transitions[(source_state, char)] = ','.join(category)
                        break

    simplifiedTransitions2 = {}
    for i in simplified_transitions:
        simplifiedTransitions2[(i[0][0],i[1])] = simplified_transitions[i][0]

    for i in simplifiedTransitions2:
        if i[0] == afdStart:
            afdStart = i[0]


    afdAcceptFinal = [] # Estados de aceptación del AFD minimizado

    for i in simplifiedTransitions2:
        if (i[0] in afdAccept) and (i[0] not in afdAcceptFinal):
            afdAcceptFinal.append(i[0])



    return AFD(afdStart,afdAccept,simplifiedTransitions2)

class AFD:
    def __init__(self, startNode, acceptanceNodes, transitions):
        self.startNode = startNode
        self.acceptanceNodes = acceptanceNodes
        self.transitions = transitions

    def getTransitions(self):
        return self.transitions
    def getStart(self):
        return self.startNode
    def getAccept(self):
        return self.acceptanceNodes

    def visualize(self):
        dot = Digraph('AFD')
        
        all_nodes = set()
        for (src, _), dest in self.transitions.items():
            all_nodes.add(src)
            all_nodes.add(dest)
        
        for node in all_nodes:
            if node in self.acceptanceNodes:
                dot.node(node, shape='doublecircle')
            else:
                dot.node(node)
        
        for (src, label), dest in self.transitions.items():
            dot.edge(src, dest, label=label)
        
        return dot
