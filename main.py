from exercises_manager import menu_ejercicios
from flashcards_manager import menu_flashcards

def menu_principal():
    while True:
        print("\n=== MENÚ PRINCIPAL ===")
        print("1) Crear o gestionar mazos de ejercicios")
        print("2) Crear o gestionar mazos de preguntas")
        print("3) Salir")

        opcion = input("Selecciona una opción: ")

        if opcion == "1":
            menu_ejercicios()
        elif opcion == "2":
            menu_flashcards()
        elif opcion == "3":
            print("👋 ¡Hasta luego! Sigue practicando matemáticas.")
            break
        else:
            print("❌ Opción inválida. Intenta nuevamente.")


if __name__ == "__main__":
    menu_principal()
