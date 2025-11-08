from flask import Flask, request, jsonify
import requests
import os 
from dotenv import load_dotenv
import json
from flask_sqlalchemy import SQLAlchemy
#from models import User, Exercise, ExerciseResult
from database import db
from utils import user_check, Save_excercise, Save_result

load_dotenv()

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")  # Ej: "postgresql://user:password@localhost:5432/ia_evaluator"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)


GEMINI_API_URL = os.getenv("GEMINI_API_URL")

@app.route('/evaluate', methods=['POST'])
def evaluate_excercise():
    try:
        data = request.get_json()  # Recibir datos en formato JSON del front
        if not data or "parts" not in data:
            return jsonify({"error": "Formato inválido: falta 'parts'"}), 400

        show_solution = data.get("show_solution", "False")  == "True"
        print("show_solution recibido:", show_solution)  # Depuración
        build_prompt(data, show_solution)  # Asegurarse de que el prompt se construye correctamente
        prompt = build_prompt(data, show_solution)
        #print("Prompt generado:", prompt)  # Depuración

        headers = {
            "Content-Type": "application/json"
        }
        payload = {
            "contents": [{
                "role": "user",
                "parts": [{"text": prompt}]
            }]
        }
        #print("Payload enviado:", payload)  # Depuración

        # Enviar al modelo Gemini
        response = requests.post(GEMINI_API_URL, headers=headers, json=payload)
        response.raise_for_status()
        gemini_output = response.json()
        print("Respuesta de la API:", gemini_output)  # Depuración

        # Procesar el campo "text" dentro de "candidates"
        text_content = gemini_output["candidates"][0]["content"]["parts"][0]["text"]
        text_content = text_content.strip()  # Eliminar espacios en blanco o caracteres adicionales
        # Eliminar las marcas de formato Markdown (```json y ```)
        if text_content.startswith("```json"):
            text_content = text_content[7:]  # Eliminar ```json
        if text_content.endswith("```"):
            text_content = text_content[:-3]  # Eliminar ```

        text_content = text_content.strip()  # Limpiar espacios adicionales
        try:
            # Convertir "text" a JSON
            parsed_json = json.loads(text_content)
            print("JSON creado exitosamente:", parsed_json)
            #operaciones de BD
            user = user_check(data)
            exercise = Save_excercise(user, data)
            Save_result(exercise, parsed_json)
            return jsonify(parsed_json), 200
        except json.JSONDecodeError as e:
            print("Error al convertir el string a JSON:", e)    
            return jsonify({"error": "El string no se pudo convertir a JSON", "raw_text": text_content}), 500
    except requests.exceptions.RequestException as e:
        print(f"Error en la solicitud: {e}")
        print("Respuesta de error:", e.response.text)  # Depuración
        return jsonify({"error": str(e)}), 500
    except Exception as e:
        print(f"Error durante la evaluación: {str(e)}")
        return jsonify({"error": str(e)}), 500

def build_prompt(data, show_solution):
    if show_solution == False:
    # Construye el texto que se envía a la IA a partir del JSON del front.
        prompt = f"Evalúa las respuestas del estudiante para el ejercicio '{data.get('title', '')}'.\n\n"
        for part in data["parts"]:
            prompt += f"Parte {part['part_id']}:\nPregunta: {part['question']}\nRespuesta: {part['student_answer']}\n\n"
            prompt += (
            "Devuelve un JSON con la siguiente estructura:\n"
            "{\n"
            "  \"feedback\": [{\"part_id\": ..., \"score\": ..., \"comment\": ...}],\n"
            "  \"overall_feedback\": ..., \n"
            "  \"exercise_passed\": true/false\n"
            "}\n"
            "El score debe ser un número entre 0 y 10. 10 siendo la mejor nota.\n"
        )
    else:
        prompt = f"Evalúa las respuestas del estudiante para el ejercicio '{data.get('title', '')}'.\n\n"
        for part in data["parts"]:
            prompt += f"Parte {part['part_id']}:\nPregunta: {part['question']}\nRespuesta: {part['student_answer']}\n"
            prompt += (
            "Devuelve un JSON con la siguiente estructura:\n"
            "{\n"
            "  \"feedback\": [{\"part_id\": ..., \"score\": ..., \"comment\": ...}],\n"
            "  \"overall_feedback\": ..., \n"
            "\"solution\": ..., \n"
            " \"exercise_passed\": true/false\n"
            "}\n"
            "El score debe ser un número entre 0 y 10. 10 siendo la mejor nota.\n"
        )
    return prompt

#No se usa actualmente
def parse_gemini_response(response_json, original_data):
    """
    Extrae el JSON generado por Gemini.
    Gemini suele devolver texto dentro de un campo como 'candidates[0].content.parts[0].text'
    """
    try:
        text = response_json["candidates"][0]["content"]["parts"][0]["text"]
        feedback_json = eval(text)  # Si devuelve texto con formato JSON, podrías usar json.loads
        feedback_json["exercise_id"] = original_data.get("exercise_id")
        return feedback_json
    except Exception as e:
        return {"error": f"Error interpretando respuesta de IA: {str(e)}"}

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)