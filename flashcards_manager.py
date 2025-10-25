import json, os, random

DATA_FILE = "data/flashcards.json"

# === Colores ANSI para gradiente confianza (1=rojo → 5=verde)
COLORES = {
    1: "\033[91m",  # rojo
    2: "\033[93m",  # amarillo
    3: "\033[33m",  # mostaza
    4: "\033[92m",  # verde claro
    5: "\033[32m",  # verde fuerte
    "RESET": "\033[0m"
}

def cargar_datos():
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, "r") as f:
        return json.load(f)

def guardar_datos(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)

# === Mostrar los mazos existentes ===
def ver_mazos():
    mazos = cargar_datos()
    if not mazos:
        print("No hay mazos de preguntas guardados.")
        return
    print("\n=== MAZOS DE PREGUNTAS ===")
    for i, m in enumerate(mazos, start=1):
        print(f"{i}) {m['nombre']} - {len(m['tarjetas'])} tarjetas")

# === Crear un nuevo mazo ===
def crear_mazo():
    mazos = cargar_datos()
    nombre = input("Nombre del mazo: ")
    cantidad = int(input("¿Cuántas tarjetas quieres agregar?: "))

    tarjetas = []
    for i in range(1, cantidad + 1):
        print(f"\nTarjeta {i}:")
        pregunta = input("Pregunta: ")
        respuesta = input("Respuesta: ")
        tarjetas.append({"pregunta": pregunta, "respuesta": respuesta, "confianza": 0})

    nuevo_mazo = {"nombre": nombre, "tarjetas": tarjetas, "puntuacion": 0}
    mazos.append(nuevo_mazo)
    guardar_datos(mazos)
    print(f"✅ Mazo '{nombre}' creado exitosamente.")

# === Eliminar un mazo ===
def eliminar_mazo():
    mazos = cargar_datos()
    ver_mazos()
    idx = int(input("Selecciona el número del mazo a eliminar: ")) - 1
    if 0 <= idx < len(mazos):
        eliminado = mazos.pop(idx)
        guardar_datos(mazos)
        print(f"🗑️ Mazo '{eliminado['nombre']}' eliminado.")
    else:
        print("❌ Número inválido.")

# === Jugar con un mazo ===
def jugar_mazo():
    mazos = cargar_datos()
    if not mazos:
        print("No hay mazos para jugar.")
        return

    ver_mazos()
    idx = int(input("Selecciona el número del mazo para jugar: ")) - 1
    if idx < 0 or idx >= len(mazos):
        print("❌ Número inválido.")
        return

    mazo = mazos[idx]
    tarjetas = mazo["tarjetas"]
    random.shuffle(tarjetas)

    print(f"\n=== JUGANDO MAZO: {mazo['nombre']} ===")
    correctas = 0

    for t in tarjetas:
        print("\nPregunta:", t["pregunta"])
        user_answer = input("Tu respuesta: ")

        if user_answer.strip().lower() == t["respuesta"].strip().lower():
            print("✅ Correcto!")
            correctas += 1
        else:
            print(f"❌ Incorrecto. Respuesta correcta: {t['respuesta']}")

        # Nivel de confianza (1–5)
        while True:
            try:
                conf = int(input("Del 1 al 5, ¿qué tan seguro estabas? "))
                if 1 <= conf <= 5:
                    t["confianza"] = conf
                    color = COLORES[conf]
                    print(f"{color}Nivel de confianza: {conf}/5{COLORES['RESET']}")
                    break
                else:
                    print("Ingresa un número entre 1 y 5.")
            except ValueError:
                print("Ingresa un número válido.")

    puntuacion = int((correctas / len(tarjetas)) * 100)
    mazo["puntuacion"] = puntuacion
    guardar_datos(mazos)

    print(f"\n🏁 Resultado final: {correctas}/{len(tarjetas)} correctas ({puntuacion}%)")
    print("Mazo actualizado con tus niveles de confianza.")

# === Mostrar estadísticas de un mazo ===
def ver_estadisticas():
    mazos = cargar_datos()
    if not mazos:
        print("No hay mazos guardados.")
        return

    ver_mazos()
    idx = int(input("Selecciona el número del mazo: ")) - 1
    if 0 <= idx < len(mazos):
        mazo = mazos[idx]
        print(f"\n=== ESTADÍSTICAS: {mazo['nombre']} ===")
        print(f"Puntuación promedio: {mazo.get('puntuacion', 0)}%")
        print("Tarjetas con sus niveles de confianza:")
        for t in mazo["tarjetas"]:
            color = COLORES.get(t["confianza"], "")
            print(f"  {color}{t['pregunta']} → Confianza: {t['confianza']}/5{COLORES['RESET']}")
    else:
        print("❌ Número inválido.")

# === Menú principal de flashcards ===
def menu_flashcards():
    while True:
        print("\n=== MENÚ DE MAZOS DE PREGUNTAS ===")
        print("1) Ver mazos")
        print("2) Crear uno nuevo")
        print("3) Eliminar un mazo")
        print("4) Jugar un mazo")
        print("5) Ver estadísticas")
        print("6) Atrás")

        opcion = input("Selecciona una opción: ")

        if opcion == "1":
            ver_mazos()
        elif opcion == "2":
            crear_mazo()
        elif opcion == "3":
            eliminar_mazo()
        elif opcion == "4":
            jugar_mazo()
        elif opcion == "5":
            ver_estadisticas()
        elif opcion == "6":
            break
        else:
            print("❌ Opción inválida.")
