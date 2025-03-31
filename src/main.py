from regex_functions import leerArchivo, shuntingYard
from afn import armarAFN
from afd import subconjuntos, minimizacion
from simulacion import simularAFN, simularAFD
from graficar import graficarAFN, graficarAFD

def main():
    data = leerArchivo()

    for i in range(len(data)):
        print('##################################################################################################################')
        print(f'Trabajando con la regex {data[i]}\n')

        # Inciso 1: Construcción infix a postfix
        postfix = shuntingYard(data[i])
        print(f'Conversión de infix a postfix: {postfix}')

        # Inciso 2: Formar el AFN de la regex
        print('Construcción del AFN...\n')
        afn = armarAFN(postfix)
        #graficarAFN(afn, i)

        # Inciso 3: Formar el AFD de la regex
        print('Construcción del AFD...\n')
        afd = subconjuntos(afn)
        #graficarAFD(afd, i)

        # Inciso 4: Formar el AFD minimizado de la regex
        print('Construcción del AFD minimizado...\n')
        afdm = minimizacion(afd)
        #graficarAFD(afdm, i, True)

        while True:
            # Mostrar el regex que está siendo evaluado
            cadena = input(f"Ingrese una cadena para probar con la regex '{data[i]}' (o escriba 'next' para pasar a la siguiente regex): ")

            if cadena.lower() == 'next':
                break

            # Inciso 5: Simulación del AFN de la regex con la cadena
            print('Simulación del AFN')
            print(simularAFN(afn, cadena), '\n')

            # Inciso 6: Simulación del AFD de la regex con la cadena
            print('Simulación del AFD')
            print(simularAFD(afd, cadena), '\n')

            # Inciso 7: Simulación del AFD minimizado de la regex con la cadena
            print('Simulación del AFD minimizado')
            print(simularAFD(afdm, cadena), '\n')
        
        print('##################################################################################################################')
        print('\n\n')
        print('Finalizado con la regex', data[i])
        print('\n\n')


if __name__ == "__main__":
    main()
