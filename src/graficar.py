import os
import logging
from graphviz import Digraph
from regex_functions import shuntingYard
from utilidades import Stack, Node

# Límite máximo de nodos para graficar
MAX_NODES = 50

# Configurar Graphviz (personaliza si tu path es diferente)
GRAPHVIZ_PATH = os.path.abspath("./Graphviz/bin")
os.environ["PATH"] += os.pathsep + GRAPHVIZ_PATH

if not os.path.exists(GRAPHVIZ_PATH):
    raise EnvironmentError(f"⚠️ Error: La carpeta '{GRAPHVIZ_PATH}' no existe. Asegúrate de que Graphviz esté instalado.")

dot_executable = os.path.join(GRAPHVIZ_PATH, "dot")
if not os.path.exists(dot_executable) and not os.path.exists(dot_executable + ".exe"):
    raise EnvironmentError(f"⚠️ Error: No se encontró 'dot' en '{GRAPHVIZ_PATH}'.")

logging.basicConfig(level=logging.INFO, format="%(message)s")

def asegurar_directorio(directorio):
    if not os.path.exists(directorio):
        os.makedirs(directorio)

def graficarAFN(afn, i):
    if afn.accept > MAX_NODES:
        print(f"⚠️ AFN demasiado grande para graficar ({afn.accept + 1} estados).")
        return

    directorio_afn = "output/afn"
    asegurar_directorio(directorio_afn)

    dot = Digraph()
    dot.attr(rankdir='LR')

    for state in range(afn.accept + 1):
        shape = "doublecircle" if state == afn.accept else "circle"
        dot.node(str(state), shape=shape)

    for (state, symbol), next_states in afn.transitions.items():
        for next_state in next_states:
            label = symbol if symbol else 'ε'
            dot.edge(str(state), str(next_state), label=label)

    dot.render(f'{directorio_afn}/afn_{i}.gv', view=False, format='jpg')

def graficarAFD(afd, i, simplified=False):
    transitions = afd.getTransitions()
    estados = set()
    for (src, _), dst in transitions.items():
        estados.add(src)
        estados.add(dst)

    if len(estados) > MAX_NODES:
        tipo = "minimizado " if simplified else ""
        print(f"⚠️ AFD {tipo}demasiado grande para graficar ({len(estados)} estados).")
        return

    directorio = "output/afdminimization" if simplified else "output/afd"
    asegurar_directorio(directorio)
    dot = afd.visualize()
    nombre_archivo = f'{directorio}/afdmin_{i}.gv' if simplified else f'{directorio}/afd_{i}.gv'
    dot.render(nombre_archivo, view=False, format='jpg')

# Árbol de expresión regular
class Tree:
    def __init__(self, root, name):
        self.root = root
        self.name = name

    def graficar(self):
        directorio_ast = "output"
        asegurar_directorio(directorio_ast)

        graph = Digraph('G', filename=f'{directorio_ast}/AST-{self.name}.gv', format='jpg')
        self.root.graficarNodo(graph)
        graph.view()

def graficarArbol(regex):
    for i, expresion in enumerate(regex):
        logging.info(f"Árbol de la expresión regular: {expresion}")
        postfix = shuntingYard(expresion)
        logging.info(f"Postfix: {postfix}")
        tree = Tree(createTree(postfix), i)
        tree.graficar()

def createTree(regex):
    stack = Stack()
    operators = ['*', '|', '.']

    for i, symbol in enumerate(regex):
        if symbol in operators:
            if symbol == '|':
                right, left = stack.pop(), stack.pop()
                node = Node(symbol, f'{i}', left, right)
            elif symbol == '.':
                right, left = stack.pop(), stack.pop()
                node = Node(symbol, f'{i}', left, right)
            elif symbol == '*':
                left = stack.pop()
                node = Node(symbol, f'{i}', left)
            stack.push(node)
        else:
            stack.push(Node(symbol, f'{i}'))

    return stack.pop()
