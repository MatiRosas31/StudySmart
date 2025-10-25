import json, os
from ai_assistant import evaluar_resultados, mostrar_informe

DATA_FILE = "data/exercises.json"

# === Funciones auxiliares ===
def cargar_datos():
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            # Si el archivo está vacío o malformado, devolvemos una lista vacía
            return []
        
def guardar_datos(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)

# === Ver mazos existentes ===
def ver_mazos():
    mazos = cargar_datos()
    if not mazos:
        print("No hay mazos de ejercicios guardados.")
        return
    print("\n=== MAZOS DE EJERCICIOS ===")
    for i, m in enumerate(mazos, start=1):
        print(f"{i}) {m['nombre']} ({m['materia']}) - {len(m['ejercicios'])} ejercicios")

# === Crear un nuevo mazo ===
def crear_mazo():
    mazos = cargar_datos()

    print("\n=== CREAR NUEVO MAZO DE EJERCICIOS ===")
    nombre = input("Nombre del mazo: ").strip()
    materia = input("Materia: ").strip()
    
    ejercicios = []
    cantidad = int(input("¿Cuántos ejercicios quieres agregar?: "))

    for i in range(1, cantidad + 1):
        print(f"\n--- Ejercicio {i} ---")
        tipo = input("¿Es un ejercicio con varias partes? (s/n): ").lower().strip()

        if tipo == "s":
            # Ejercicio con sub-preguntas
            letra_principal = input("Letra de la consigna principal (ej. a, b, c o 1, 2, 3): ").strip()
            estilo = input("¿Las sub-consignas serán con letras (a,b,c) o números (1,2,3)? (l/n): ").lower().strip()
            sub_cantidad = int(input("¿Cuántas sub-consignas tendrá?: "))

            sub_cons = []
            for j in range(sub_cantidad):
                if estilo == "l":
                    etiqueta = chr(97 + j)  # a, b, c, ...
                else:
                    etiqueta = str(j + 1)   # 1, 2, 3, ...
                
                consigna = input(f"Escribe la consigna ({letra_principal} {etiqueta}): ").strip()
                solucion = input(f"Escribe la SOLUCION ahora ({letra_principal} {etiqueta}): ").strip()
                sub_cons.append({"id": f"{letra_principal}{etiqueta}", "consigna": consigna, "solucion": solucion})

            ejercicios.append({
                "tipo": "multiple",
                "letra_principal": letra_principal,
                "sub_cons": sub_cons
            })

        else:
            # Ejercicio simple
            consigna = input("Escribe la consigna: ").strip()
            solucion = input("Escribe la solución: ").strip()
            ejercicios.append({
                "tipo": "simple",
                "consigna": consigna,
                "solucion": solucion
            })

    nuevo_mazo = {
        "nombre": nombre,
        "materia": materia,
        "ejercicios": ejercicios
    }

    mazos.append(nuevo_mazo)
    guardar_datos(mazos)
    print(f"\n✅ Mazo '{nombre}' guardado correctamente.\n")

# === Eliminar un mazo ===
def eliminar_mazo():
    mazos = cargar_datos()
    ver_mazos()
    if not mazos:
        return
    idx = int(input("Selecciona el número del mazo a eliminar: ")) - 1
    if 0 <= idx < len(mazos):
        eliminado = mazos.pop(idx)
        guardar_datos(mazos)
        print(f"🗑️ Mazo '{eliminado['nombre']}' eliminado.")
    else:
        print("❌ Número inválido.")

# === Practicar un mazo de ejercicios ===
def practicar_mazo():
    mazos = cargar_datos()
    if not mazos:
        print("No hay mazos para practicar.")
        return

    ver_mazos()
    idx = int(input("Selecciona el número del mazo para practicar: ")) - 1
    if idx < 0 or idx >= len(mazos):
        print("❌ Número inválido.")
        return

    mazo = mazos[idx]
    respuestas_usuario = []
    soluciones = []
    niveles_confianza = []

    print(f"\n=== PRACTICANDO: {mazo['nombre']} ===")

    for i, e in enumerate(mazo["ejercicios"], start=1):
        print(f"\nEjercicio {i}: {e['consigna']}")
        r = input("Tu respuesta: ")
        respuestas_usuario.append(r)
        soluciones.append(e["solucion"])

        while True:
            try:
                conf = int(input("Nivel de confianza (1–5): "))
                if 1 <= conf <= 5:
                    niveles_confianza.append(conf)
                    break
                else:
                    print("Ingresa un número entre 1 y 5.")
            except ValueError:
                print("Ingresa un número válido.")

    # Evaluar resultados con el asistente de IA
    resultado = evaluar_resultados(respuestas_usuario, soluciones, niveles_confianza)
    mostrar_informe(resultado)

# === Menú principal de mazos de ejercicios ===
def menu_ejercicios():
    while True:
        print("\n=== MENÚ DE MAZOS DE EJERCICIOS ===")
        print("1) Ver mazos")
        print("2) Crear uno nuevo")
        print("3) Eliminar un mazo")
        print("4) Practicar un mazo")
        print("5) Atrás")

        opcion = input("Selecciona una opción: ")

        if opcion == "1":
            ver_mazos()
        elif opcion == "2":
            crear_mazo()
        elif opcion == "3":
            eliminar_mazo()
        elif opcion == "4":
            practicar_mazo()
        elif opcion == "5":
            break
        else:
            print("❌ Opción inválida.")
