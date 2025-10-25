import statistics
import random

# Frases de retroalimentación según desempeño
FRASES_EXCELENTE = [
    "Excelente trabajo 👏",
    "¡Dominás este tema!",
    "¡Tu lógica matemática está afilada!"
]

FRASES_BUENO = [
    "Vas muy bien, pero podrías repasar algunos conceptos.",
    "Buen desempeño, ¡seguí así!",
    "Solo unos pocos errores, estás progresando."
]

FRASES_MEJORAR = [
    "Necesitás reforzar la práctica en este tema.",
    "Cometiste varios errores, revisá los fundamentos.",
    "No te preocupes, lo importante es seguir practicando."
]


def evaluar_resultados(respuestas_usuario, soluciones_correctas, niveles_confianza):
    """
    Analiza el desempeño del usuario y devuelve un informe con:
    - Puntuación general
    - Preguntas incorrectas
    - Análisis de confianza
    - Recomendaciones
    """

    total = len(soluciones_correctas)
    correctas = 0
    errores = []

    for i, (r_usuario, r_correcta) in enumerate(zip(respuestas_usuario, soluciones_correctas)):
        if str(r_usuario).strip().lower() == str(r_correcta).strip().lower():
            correctas += 1
        else:
            errores.append({
                "nro": i + 1,
                "esperado": r_correcta,
                "dado": r_usuario
            })

    # Puntuación base
    score = round((correctas / total) * 100, 2)

    # Promedio de confianza
    conf_prom = round(statistics.mean(niveles_confianza), 2) if niveles_confianza else 0

    # Calcular “precisión emocional”: diferencia entre confianza y rendimiento
    desviacion_confianza = abs(conf_prom - (score / 20))  # normaliza score 0–100 → 0–5

    # Generar feedback textual
    if score >= 90:
        feedback = random.choice(FRASES_EXCELENTE)
    elif score >= 70:
        feedback = random.choice(FRASES_BUENO)
    else:
        feedback = random.choice(FRASES_MEJORAR)

    # Recomendaciones específicas
    recomendaciones = []
    if errores:
        recomendaciones.append("🔁 Repetí los ejercicios que fallaste.")
    if conf_prom < 3:
        recomendaciones.append("💡 Aumentá tu confianza practicando ejercicios similares.")
    if desviacion_confianza > 2:
        recomendaciones.append("⚖️ Tu nivel de confianza no coincide con tu precisión. Revisá tus estimaciones.")
    if not recomendaciones:
        recomendaciones.append("🌟 Seguí practicando con nuevos desafíos.")

    resultado = {
        "total": total,
        "correctas": correctas,
        "score": score,
        "confianza_promedio": conf_prom,
        "errores": errores,
        "feedback": feedback,
        "recomendaciones": recomendaciones
    }

    return resultado


def mostrar_informe(resultado):
    """Muestra en consola el análisis del asistente."""
    print("\n=== INFORME DEL ASISTENTE DE APRENDIZAJE ===")
    print(f"Ejercicios correctos: {resultado['correctas']} / {resultado['total']}")
    print(f"Puntuación: {resultado['score']}%")
    print(f"Nivel de confianza promedio: {resultado['confianza_promedio']}/5")
    print(f"Retroalimentación: {resultado['feedback']}")
    print("\nRecomendaciones:")
    for r in resultado["recomendaciones"]:
        print(f" - {r}")

    if resultado["errores"]:
        print("\nErrores detectados:")
        for e in resultado["errores"]:
            print(f"  ❌ Ejercicio {e['nro']}: respondiste '{e['dado']}', debía ser '{e['esperado']}'")

    print("\n============================================")
