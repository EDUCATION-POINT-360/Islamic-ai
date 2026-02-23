import os
import requests
import google.generativeai as genai
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# ---------------------------------------------------------
# 1. GEMINI CONFIGURATION
# ---------------------------------------------------------
# Yahan apni API Key dalein (https://aistudio.google.com/)
GEMINI_API_KEY = "AIzaSyAabkcFTfJvbS8j3oqz4qLQbdmylppdgVw"
genai.configure(api_key=GEMINI_API_KEY)

# Gemini Model Setup with System Instruction
model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    system_instruction=(
        "You are an authentic and helpful Islamic AI Assistant. "
        "Your goal is to provide accurate information from the Quran and Hadith. "
        "1. Use Markdown for formatting (bold, lists, etc.). "
        "2. Always mention Surah name and Ayah number for Quranic references. "
        "3. If providing an Arabic verse, wrap it like this: <div class='arabic-text'>ARABIC_HERE</div> "
        "4. Answer in a mix of Urdu and English (Roman Urdu/Hindi) that is easy to understand. "
        "5. If you are unsure, advise the user to consult a qualified scholar."
    )
)

# ---------------------------------------------------------
# 2. QURAN API HELPER
# ---------------------------------------------------------
def fetch_quran_references(query):
    """Quran API se relevant verses dhoondne ke liye"""
    try:
        # English translation search for better context matching
        search_url = f"https://api.alquran.cloud/v1/search/{query}/all/en.sahih"
        response = requests.get(search_url).json()
        
        if response['code'] == 200 and response['data']['count'] > 0:
            matches = response['data']['matches'][:3]  # Top 3 results
            context_text = "Relevant Quranic Verses:\n"
            for m in matches:
                context_text += f"- Surah {m['surah']['englishName']} ({m['numberInSurah']}): {m['text']}\n"
            return context_text
    except Exception as e:
        print(f"Quran API Error: {e}")
    return ""

# ---------------------------------------------------------
# 3. MAIN CHAT ROUTE
# ---------------------------------------------------------
@app.route('/ask', methods=['POST'])
def ask_ai():
    data = request.json
    user_query = data.get('query', '')

    if not user_query:
        return jsonify({"answer": "Please ask a question."}), 400

    # Step 1: Get data from Quran API
    quran_context = fetch_quran_references(user_query)

    # Step 2: Combine query and context for Gemini
    final_prompt = f"User Question: {user_query}\n\nContextual Data:\n{quran_context}"

    try:
        # Step 3: Generate response using Gemini
        chat_response = model.generate_content(final_prompt)
        
        return jsonify({
            "answer": chat_response.text,
            "has_context": len(quran_context) > 0
        })

    except Exception as e:
        return jsonify({"answer": f"Gemini API Error: {str(e)}"}), 500

# ---------------------------------------------------------
# 4. RUN SERVER
# ---------------------------------------------------------
if __name__ == '__main__':
    print("Islamic AI Server is starting on http://127.0.0.1:5000")
    app.run(debug=True, port=5000)
    
