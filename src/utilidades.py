class Stack:
    def __init__(self):
        self.items = []

    def push(self, item):
        self.items.append(item)
    
    def pop(self):
        return self.items.pop()
    
    def isEmpty(self):
        return self.items == []

    def peek(self):
        if len(self.items) == 0:
            return 
        else:
            return self.items[len(self.items)-1]
    
    def size(self):
        return len(self.items)

class Node:
    def __init__(self, value, identifier):
        self.value = value
        self.identifier = identifier
        self.left = None
        self.right = None
    def graficarNodo(self, g):
        g.node(self.identifier, label=str(self.value))
        if self.left != None:
            g.edge(self.identifier, self.left.identifier)
            self.left.graficarNodo(g)
        if self.right != None:
            g.edge(self.identifier, self.right.identifier)
            self.right.graficarNodo(g)

def conjuntoToString(setx):
    string = ''
    for i in range(len(list(setx))):
        if i < len(setx)-1:
            string += str(list(setx)[i])+','
        else:
            string += str(list(setx)[i])
    return string