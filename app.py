import os
import requests
import google.generativeai as genai
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# ---------------------------------------------------------
# 1. API CONFIGURATION
# ---------------------------------------------------------
# Apni Keys yahan enter karein
GEMINI_API_KEY = "AIzaSyAabkcFTfJvbS8j3oqz4qLQbdmylppdgVw"
HADITH_API_KEY = "$2y$10$MhCtBc8HwW7yNtV8NvrNPOYPoIuhwFlJFDIUcb9agVna9Bjkwa2H6" # Aapki share ki hui key

genai.configure(api_key=GEMINI_API_KEY)

# Gemini Model Setup
model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    system_instruction=(
        "You are an Islamic Scholar AI. Answer based on Quran and the provided Hadith context. "
        "1. Use Markdown for styling. "
        "2. Use <div class='arabic-text'>...</div> for Arabic script. "
        "3. Always mention the source (Surah/Ayah or Hadith Book/Chapter). "
        "4. Language: Roman Urdu/Hindi mixed with English."
    )
)

# ---------------------------------------------------------
# 2. FETCHING LOGIC
# ---------------------------------------------------------

def get_quran_context(query):
    try:
        url = f"https://api.alquran.cloud/v1/search/{query}/all/en.sahih"
        res = requests.get(url).json()
        if res['code'] == 200 and res['data']['count'] > 0:
            match = res['data']['matches'][0]
            return f"Quran: Surah {match['surah']['englishName']} ({match['numberInSurah']}) - {match['text']}"
    except: return ""
    return ""

def get_hadith_context(query):
    """Hadith API (hadithapi.com) integration"""
    try:
        # Search endpoint for Hadith API
        url = f"https://hadithapi.com/api/hadiths?apiKey={HADITH_API_KEY}&paginate=1&hadithEnglish={query}"
        res = requests.get(url).json()
        
        if 'hadiths' in res and 'data' in res['hadiths'] and len(res['hadiths']['data']) > 0:
            h = res['hadiths']['data'][0]
            book = h.get('bookName', 'Hadith')
            text = h.get('hadithEnglish', '')
            chapter = h.get('chapterName', '')
            return f"Hadith Source: {book} (Chapter: {chapter}) - {text}"
    except Exception as e:
        print(f"Hadith API Error: {e}")
    return ""

# ---------------------------------------------------------
# 3. CHAT ENDPOINT
# ---------------------------------------------------------

@app.route('/ask', methods=['POST'])
def ask():
    user_query = request.json.get('query', '')
    if not user_query:
        return jsonify({"answer": "Sawal likhiye..."}), 400

    # Parallel Data Fetching
    q_data = get_quran_context(user_query)
    h_data = get_hadith_context(user_query)
    
    combined_context = f"REFERENCES FOUND:\n{q_data}\n\n{h_data}"

    try:
        # Sending everything to Gemini
        prompt = f"User Question: {user_query}\n\nReferences:\n{combined_context}\n\nProvide an authentic answer:"
        response = model.generate_content(prompt)
        
        return jsonify({
            "answer": response.text,
            "debug_context": combined_context # For testing
        })
    except Exception as e:
        return jsonify({"answer": f"System Error: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)
    
