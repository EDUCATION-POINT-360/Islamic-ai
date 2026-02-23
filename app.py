import streamlit as st
import google.generativeai as genai

# Page Configuration
st.set_page_config(page_title="Islamic AI Guide", page_icon="🌙")

# Sidebar for Branding
with st.sidebar:
    st.title("🌙 Al-Huda AI")
    st.info("Yeh AI Quran aur Sahih Hadith ki roshni mein jawab deta hai.")
    st.markdown("---")
    st.write("Maqsad: Islam ki sahi taleem phailana.")

# API Key Connection (Aapko apni key yahan daalni hogi)
genai.configure(api_key="AIzaSyAaW2MPeWEkpBAhgsLKV7kBTVHR-qnL75s")

# System Prompt (AI ko sikhane ke liye)
system_instruction = "Aap ek expert Islamic Scholar hain. Har sawal ka jawab Quran aur Sahih Bukhari/Muslim ke hawale se dein. Agar koi baat confirm na ho toh maafi maang lein lekin galat maloomat na dein."

model = genai.GenerativeModel('gemini-1.5-flash-latest')

# Main Interface
st.header("Assalamu Alaikum! Aapka Deeni Sawal Kya Hai?")
user_input = st.chat_input("Yahan apna sawal likhein (Urdu/Hindi/English)...")

if user_input:
    with st.chat_message("user"):
        st.write(user_input)
    
    with st.chat_message("assistant"):
        with st.spinner("Dalail talash kiye ja rahe hain..."):
            response = model.generate_content(f"{system_instruction} \n Question: {user_input}")
            st.write(response.text)
            st.caption("Note: Yeh AI maloomat ke liye hai. Bade masail mein Mufti se ruju karein.")
            
