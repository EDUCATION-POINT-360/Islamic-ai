import requests
import google.generativeai as genai
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
# CORS enable karna zaroori hai taake frontend connect ho sake
CORS(app)

# --- CONFIGURATION ---
GEMINI_API_KEY = "AIzaSyAabkcFTfJvbS8j3oqz4qLQbdmylppdgVw"
HADITH_API_KEY = "$2y$10$MhCtBc8HwW7yNtV8NvrNPOYPoIuhwFlJFDIUcb9agVna9Bjkwa2H6"

genai.configure(api_key=GEMINI_API_KEY)

model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    system_instruction=(
        "You are an Islamic Scholar AI. Answer based on Quran and Hadith references. "
        "Use Markdown for formatting. Use <div class='arabic-text'>...</div> for Arabic script. "
        "Always provide Surah/Ayah or Hadith Book names. Language: Roman Urdu/Hindi + English."
    )
)

# --- DATA FETCHING ---
def get_quran(query):
    try:
        url = f"https://api.alquran.cloud/v1/search/{query}/all/en.sahih"
        res = requests.get(url).json()
        if res['code'] == 200 and res['data']['count'] > 0:
            m = res['data']['matches'][0]
            return f"Quran: Surah {m['surah']['englishName']} ({m['numberInSurah']}) - {m['text']}"
    except: return ""
    return ""

def get_hadith(query):
    try:
        url = f"https://hadithapi.com/api/hadiths?apiKey={HADITH_API_KEY}&paginate=1&hadithEnglish={query}"
        res = requests.get(url).json()
        if 'hadiths' in res and res['hadiths']['data']:
            h = res['hadiths']['data'][0]
            return f"Hadith: {h['bookName']} - {h['hadithEnglish']}"
    except: return ""
    return ""

# --- ROUTE ---
@app.route('/ask', methods=['POST'])
def ask():
    user_query = request.json.get('query', '')
    q_ref = get_quran(user_query)
    h_ref = get_hadith(user_query)
    
    context = f"References:\n{q_ref}\n{h_ref}"
    prompt = f"Question: {user_query}\n\nContext:\n{context}\n\nProvide an authentic answer:"

    try:
        response = model.generate_content(prompt)
        return jsonify({"answer": response.text})
    except Exception as e:
        return jsonify({"answer": f"Backend Error: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)
    
