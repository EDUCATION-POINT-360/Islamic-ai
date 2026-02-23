import streamlit as st
import google.generativeai as genai

# Page Setup
st.set_page_config(page_title="Al-Huda AI", page_icon="🌙")

# Sidebar
with st.sidebar:
    st.title("🌙 Al-Huda AI")
    st.info("Quran aur Sahih Hadith ki roshni mein jawab.")

# 1. API Key Setup (Yahan apni sahi key dalein)
API_KEY = "YOUR_GEMINI_API_KEY_HERE"
genai.configure(api_key=API_KEY)

# 2. Model Selection (Updated Version)
# 'gemini-1.5-flash' ki jagah hum 'gemini-pro' try karenge agar wo nahi chal raha
try:
    model = genai.GenerativeModel('gemini-1.5-flash')
except:
    model = genai.GenerativeModel('gemini-pro')

system_instruction = "Aap ek Islamic Scholar hain. Quran aur Sahih Hadith se jawab dein."

# UI
st.header("Assalamu Alaikum! Aapka Deeni Sawal Kya Hai?")

if "messages" not in st.session_state:
    st.session_state.messages = []

# Chat history dikhane ke liye
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# User input
if user_input := st.chat_input("Yahan sawal likhein..."):
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    with st.chat_message("assistant"):
        try:
            # AI Response
            full_prompt = f"{system_instruction}\nUser Question: {user_input}"
            response = model.generate_content(full_prompt)
            
            st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
        except Exception as e:
            st.error(f"Error: AI Connect nahi ho pa raha. Apni API Key check karein. Details: {e}")
            
