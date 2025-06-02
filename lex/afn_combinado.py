# Código: afn_combinado.py
class AFN:
    def __init__(self, start, accept, transitions):
        self.start = start
        self.accept = accept
        self.transitions = transitions
        self.token_id = None
        self.token_name = None

    def getTransitions(self):
        return self.transitions

    def getStart(self):
        return self.start

    def getAccept(self):
        return self.accept


def combinar_afns(lista_afns):
    new_start = 0
    current_offset = 1
    transitions = {}

    accept_states = []
    token_map = {}

    for afn in lista_afns:
        offset = current_offset
        offset_transitions = {}

        for (state, symbol), next_states in afn.getTransitions().items():
            new_key = (state + offset, symbol)
            new_vals = [n + offset for n in next_states]
            offset_transitions[new_key] = new_vals

        # Copiar las transiciones
        transitions.update(offset_transitions)

        # Agregar transición ε desde el nuevo estado inicial
        if (new_start, '') not in transitions:
            transitions[(new_start, '')] = []

        transitions[(new_start, '')].append(afn.getStart() + offset)

        # Mapear estado de aceptación al token
        accept_states.append(afn.getAccept() + offset)
        accept_state = afn.getAccept() + offset
        if accept_state not in token_map or afn.token_id < token_map[accept_state][0]:
            token_map[accept_state] = (afn.token_id, afn.token_name)


        current_offset += afn.getAccept() + 1  # salto suficiente

    # Guardar info del token en el objeto AFN combinado
    afn_completo = AFN(new_start, accept_states, transitions)
    afn_completo.token_map = token_map
    afn_completo.accept_states = accept_states
    return afn_completo
