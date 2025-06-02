# Código: simulacion.py
import random
import copy

def findPath(path, afnTransitions, afnAccept, string, index):
    if index < len(string):
        if (path[-1] != afnAccept) and (index < len(string)):
            for i in afnTransitions:
                if path[-1] in i:
                    if (path[-1], string[index]) in afnTransitions:
                        for j in afnTransitions[(path[-1], string[index])]:
                            j = random.choice(afnTransitions[(path[-1], string[index])])
                            try:
                                newPath = (copy.deepcopy(path))
                                newPath.append(j)
                                newPath = findPath(newPath, afnTransitions, afnAccept, string, index+1) 
                                if type(newPath) == type(None):
                                    continue
                                else:
                                    return newPath
                            except:
                                continue
                    elif (path[-1],'ε') in afnTransitions:

                            for j in afnTransitions[(path[-1],'ε')]:
                                j = random.choice(afnTransitions[(path[-1],'ε')])
                                try:
                                    newPath = (copy.deepcopy(path))
                                    newPath.append(j)
                                    newPath = findPath(newPath, afnTransitions, afnAccept, string, index)
                                    if type(newPath) == type(None):
                                        continue
                                    else:
                                        return newPath
                                except:
                                    continue
                    else:
                        return None
    elif (index >= len(string)):
        if (path[-1] == afnAccept) and (index >= len(string)):
            return path

        for i in afnTransitions:
            if path[-1] in i:
                if (path[-1],'ε') in afnTransitions:
                    for j in afnTransitions[(path[-1],'ε')]:
                        j = random.choice(afnTransitions[(path[-1],'ε')])
                        try:
                            newPath = (copy.deepcopy(path))
                            newPath.append(j)
                            newPath = findPath(newPath, afnTransitions, afnAccept, string, index)
                            if type(newPath) == type(None):
                                continue
                            else:
                                return newPath
                        except:
                            continue

def simularAFN(afn, string):
    if string == '':
        string = 'ε'

    afnTransitions = afn.getTransitions()
    afnStart = afn.getStart()
    afnAccept = afn.getAccept()

    afnTransitions2 = {}
    for i in afnTransitions:
        if i[1] == '':
            afnTransitions2[(i[0],'ε')] = afnTransitions[i]
        else:
            afnTransitions2[i] = afnTransitions[i]

    afnTransitions = afnTransitions2

    allchars = []
    for i in afnTransitions:
        if i[1] not in allchars:
            allchars.append(i[1])
    allchars.append('')

    states = []
    for i in afnTransitions.keys():
        states.append(i[0])
    states.append(afnAccept)

    charKleene = {}

    
    for i in states:
        epsilonKleene = [i]
        changed = True
        while changed:
            changed = False
            for j in epsilonKleene:
                if (j, 'ε') in afnTransitions:
                    for k in afnTransitions[(j, 'ε')]:
                        if k not in epsilonKleene:
                            epsilonKleene.append(k)
                            changed = True
        charKleene[i] = sorted(epsilonKleene)

    for i in string:
        if i not in allchars:
            return "La cadena NO es aceptada porque tiene caracteres no aceptados"

    for i in range(1000):
        path = findPath([afnStart], afnTransitions, afnAccept, string,0)
        if type(path) == type(None):
            continue
        else:
            break

    if type(path) == type(None):
        return "La cadena NO es aceptada"

    print(path)
    if path[-1] == afnAccept:
        return f'La cadena SI es aceptada'
    else:
        return f'La cadena NO es aceptada'

def simularAFD(afd, string):

    string = string.replace('ε','')

    afdTransitions = afd.getTransitions()
    afdStart = afd.getStart()
    afdAccept = afd.getAccept()

    path = f'{afdStart}'
    currentState = afdStart

    for i in string:
        if (currentState, i) in afdTransitions:
            currentState = afdTransitions[(currentState, i)]
            path += f' =>({i}) {currentState}'
        else:
            return "La cadena NO es aceptada"


    if currentState in afdAccept:
        print('Path:\n',path)
        return "La cadena SI es aceptada"
    else:
        return "La cadena NO es aceptada"