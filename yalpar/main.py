# main.py

import sys
import importlib.util
import os

def cargar_modulo_desde_ruta(nombre_modulo, ruta_archivo):
    """
    Carga dinámicamente un módulo de Python a partir de la ruta de su archivo .py.
    """
    spec = importlib.util.spec_from_file_location(nombre_modulo, ruta_archivo)
    if spec is None:
        raise ImportError(f"No se pudo crear spec para {ruta_archivo}")
    módulo = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(módulo)
    sys.modules[nombre_modulo] = módulo
    return módulo

def run_parser_srl2(
    ruta_test,
    ruta_lexer_py="slr2_lexer.py",
    ruta_parser_py="yalpar/output/parser_slr2.py",
    ruta_salida_log="output/yalpar/resultado_parser2.txt"
):
    # 0) Abrir archivo de log
    try:
        archivo = open(ruta_salida_log, "w", encoding="utf-8")
    except IOError as e:
        print(f"Error al crear {ruta_salida_log}: {e}")
        sys.exit(1)

    # 1) Verificar que existan los archivos del lexer y parser
    if not os.path.isfile(ruta_lexer_py):
        archivo.write(f"Error: no encontré {ruta_lexer_py}\n")
        archivo.close()
        sys.exit(1)
    if not os.path.isfile(ruta_parser_py):
        archivo.write(f"Error: no encontré {ruta_parser_py}\n")
        archivo.close()
        sys.exit(1)

    # 2) Cargar dinámicamente el módulo del lexer
    módulo_lexer = cargar_modulo_desde_ruta("mi_lexer", ruta_lexer_py)
    if not hasattr(módulo_lexer, "analizar"):
        archivo.write(f"El archivo {ruta_lexer_py} no define 'analizar(texto)'.\n")
        archivo.close()
        sys.exit(1)
    analizar = módulo_lexer.analizar

    # 3) Cargar dinámicamente el módulo del parser
    módulo_parser = cargar_modulo_desde_ruta("mi_parser", ruta_parser_py)
    if not hasattr(módulo_parser, "parse"):
        archivo.write(f"El archivo {ruta_parser_py} no define 'parse(tokens)'.\n")
        archivo.close()
        sys.exit(1)
    parse = módulo_parser.parse

    # 4) Leer el archivo de pruebas (cada línea es una cadena a evaluar)
    try:
        with open(ruta_test, "r", encoding="utf-8") as f:
            líneas = [línea.strip() for línea in f if línea.strip()]
    except FileNotFoundError:
        archivo.write(f"Error: no existe el archivo de pruebas '{ruta_test}'\n")
        archivo.close()
        sys.exit(1)

    # 5) Procesar cada línea: tokenizar, agregar ('$','$'), parsear y registrar en el log
    for idx, texto in enumerate(líneas, start=1):
        # 5.1) Tokenizar sin concatenar " $"
        tokens = analizar(texto)
        # 5.2) Agregar el token fin de entrada ('$', '$')
        tokens.append(('$', '$'))

        archivo.write(f"\n=== Línea {idx}: «{texto}»\n")
        archivo.write(f"Tokens obtenidos por el lexer: {tokens}\n")
        aceptada = parse(tokens)
        if aceptada:
            archivo.write(f"---> Línea {idx} → ACEPTADA.\n")
        else:
            archivo.write(f"---> Línea {idx} → RECHAZADA.\n")

    archivo.close()

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Uso: python main.py <ruta_archivo_de_pruebas>")
        print("Ejemplo: python main.py input/txt/number_expressions.txt")
        sys.exit(1)

    ruta = sys.argv[1]
    run_parser_srl2(
        ruta,
        ruta_lexer_py="output/lexer.py",
        ruta_parser_py="yalpar/output/parser_slr2.py",
        ruta_salida_log="output/yalpar/slr2_variable.txt"
    )