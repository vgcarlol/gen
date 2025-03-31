# Código: definicion_expander.py
def expandir_definiciones(data):
    definiciones = data['definitions']
    tokens = data['tokens']

    def expandir(expr):
        # 1) Si expr coincide EXACTAMENTE con un nombre de definición y no contiene {} ni comillas:
        if '{' not in expr and '}' not in expr and "'" not in expr and '"' not in expr:
            # Separar por espacios en caso de que fueran varias partes
            partes = expr.split()
            # Si es una sola palabra y coincide con definiciones, expandimos
            if len(partes) == 1 and partes[0] in definiciones:
                return expandir(definiciones[partes[0]])

        resultado = ''
        i = 0
        while i < len(expr):
            if expr[i] in ["'", '"']:
                # 2) Detectar literales entre '...' o "..."
                quote = expr[i]
                j = i + 1
                while j < len(expr) and expr[j] != quote:
                    j += 1
                literal = expr[i+1:j]

                # Escapar metacaracteres en ese literal
                escaped_literal = ''
                for ch in literal:
                    if ch in ".|*+?()":
                        escaped_literal += f"\\{ch}"
                    else:
                        escaped_literal += ch

                # Envolver en paréntesis para que sea un solo grupo
                resultado += f'({escaped_literal})'
                i = j + 1

            elif expr[i] == '{':
                # 3) Expandir recursivamente definiciones let {nombre}
                j = i + 1
                while j < len(expr) and expr[j] != '}':
                    j += 1
                nombre = expr[i+1:j]
                if nombre in definiciones:
                    reemplazo = expandir(definiciones[nombre])
                    resultado += f'({reemplazo})'
                else:
                    raise ValueError(f"Referencia a definición desconocida: {nombre}")
                i = j + 1

            else:
                resultado += expr[i]
                i += 1

        return resultado

    tokens_expandidos = []
    for regex, token in tokens:
        print(f"🔍 Regex expandida (original): {regex} -> Token: {token}")
        expresion_expandida = expandir(regex)
        tokens_expandidos.append((expresion_expandida, token))

    return tokens_expandidos
