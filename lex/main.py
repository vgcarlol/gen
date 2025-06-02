# main.py

from yal_parser import leerYAL
from definicion_expander import expandir_definiciones
from regex_functions import shuntingYard
from afn import armarAFN
from afd import subconjuntos
from afn_combinado import combinar_afns
from lexer_generator import generar_lexer_py

import pickle
import os

def main():
    # 1) Leer archivo .yal
    archivo_yal = './input/yal/slr-4.yal'
    datos = leerYAL(archivo_yal)

    print("=== PARSER DE YAL ===")
    print(f"Definitions leidas: {datos['definitions']}")
    if 'rules' in datos:
        for ruleinfo in datos['rules']:
            print(f"  Regla: {ruleinfo['name']} [args={ruleinfo['args']}] => tokens: {ruleinfo['tokens']}")
    print(f"Tokens combinados: {datos['tokens']}")

    # 2) Expandir definiciones
    tokens_expandidos = expandir_definiciones(datos)
    print("\n=== EXPANSION DE DEFINICIONES ===")
    for i, (expreg, tkn) in enumerate(tokens_expandidos):
        print(f" {i+1}) Token={tkn}, Regex expandida='{expreg}'")

    # 3) Construir AFNs
    token_afns = []
    id_counter = 1
    print("\n=== CONSTRUCCION DE AFNs POR TOKEN ===")
    for (expanded_regex, token_name) in tokens_expandidos:
        print(f"\n-> Procesando token='{token_name}' con regex='{expanded_regex}'")
        try:
            postfix = shuntingYard(expanded_regex)
            afn = armarAFN(postfix)
            afn.token_id = id_counter
            afn.token_name = token_name or f"TOKEN_{id_counter}"
            token_afns.append(afn)
            id_counter += 1
        except Exception as e:
            print(f"❌ Error al procesar token='{token_name}' => {e}")
            continue

    print(f"\n--- Se construyeron {len(token_afns)} AFNs. ---")

    # 4) Combinar AFNs en uno
    afn_completo = combinar_afns(token_afns)
    if hasattr(afn_completo, 'token_map'):
        print("token_map:", afn_completo.token_map)

    # 5) Subconjuntos => AFD
    afd_final = subconjuntos(afn_completo)
    print("start:", afd_final.getStart())
    print("accept:", afd_final.getAccept())

    # ————————— Serializar el DFA para parser.py —————————
    os.makedirs("./output/lexers", exist_ok=True)
    with open("./output/lexers/dfa.pickle", "wb") as f:
        pickle.dump(afd_final, f)
    print("✅ DFA guardado en: output/lexers/dfa.pickle")
    # ————————————————————————————————————————————————

    # 6) Generar lexer
    generar_lexer_py(afd_final, afn_completo.token_map)
    print("\n✅ lexer.py generado en output/lexer.py. Ya puedes usarlo con input/codigo.txt")


if __name__ == "__main__":
    main()
