# -*- coding: utf-8 -*-
import streamlit as st
from dotenv import load_dotenv
import os
import requests
from langdetect import detect
import emoji

# Load environment variables
load_dotenv()
HUGGINGFACE_API_KEY = os.getenv("HUGGINGFACE_API_KEY")

# Helper function to call Hugging Face LLM
def generate_questions(tech_stack):
    """
    Generate technical questions based on the tech stack using Hugging Face model.
    """
    model = "mistralai/Mistral-7B-Instruct-v0.1"  # You can replace this with another model
    url = f"https://api-inference.huggingface.co/models/{model}"
    
    headers = {
        "Authorization": f"Bearer {HUGGINGFACE_API_KEY}"
    }
    
    prompt = f"Generate 5 interview questions for {tech_stack}."
    
    payload = {
        "inputs": prompt,
        "parameters": {
            "max_length": 500,
            "temperature": 0.7,
            "top_p": 0.9
        }
    }

    response = requests.post(url, headers=headers, json=payload)
    
    if response.status_code == 200:
        result = response.json()[0]['generated_text']
        return result
    else:
        return "⚠️ Error generating questions. Please try again."

# Multilingual Support
from langdetect import detect, DetectorFactory

# Ensuring consistent language detection
DetectorFactory.seed = 0  

def detect_language(text):
    try:
        lang = detect(text)
        # Force default to English if detected language seems incorrect
        if lang not in ["en", "fr", "es", "de"]:  # Allow only common languages
            return "en"
        return lang
    except:
        return "en"  # Default to English in case of error
# Sentiment Analysis (Basic Simulation)
def analyze_sentiment(message):
    positive_words = ["good", "excellent", "awesome", "love", "like", "positive", "great"]
    negative_words = ["bad", "poor", "terrible", "hate", "dislike", "negative", "awful"]

    message = message.lower()
    
    if any(word in message for word in positive_words):
        return emoji.emojize(":smiley: Positive")
    elif any(word in message for word in negative_words):
        return emoji.emojize(":pensive: Negative")
    else:
        return emoji.emojize(":neutral_face: Neutral")

# Streamlit UI
st.title("🚀 TalentScout Hiring Assistant")

# Greeting message
st.sidebar.image("https://via.placeholder.com/150", caption="TalentScout AI")
st.sidebar.write("Welcome to TalentScout! Please enter your details to get started.")

# Candidate Information Form
name = st.text_input("👤 Full Name")
email = st.text_input("📧 Email Address")
phone = st.text_input("📱 Phone Number")
experience = st.slider("💼 Years of Experience", 0, 30, 1)
position = st.text_input("🎯 Desired Position")
location = st.text_input("🌍 Current Location")

# Tech Stack Input
tech_stack = st.text_area("🛠️ Enter your tech stack (e.g., Python, Django, React, AWS)")

# Language detection
if tech_stack:
    language = detect_language(tech_stack)
    st.write(f"🌐 Detected Language: {language.upper()}")

# Submit Button
if st.button("Generate Technical Questions"):
    if all([name, email, phone, experience, position, location, tech_stack]):
        with st.spinner("Generating technical questions..."):
            questions = generate_questions(tech_stack)
            st.success("✅ Questions generated successfully!")
            st.write(questions)
            
            # Simulate Sentiment Analysis
            sentiment = analyze_sentiment(questions)
            st.write(f"🧠 Sentiment Analysis: {sentiment}")
    else:
        st.warning("⚠️ Please fill in all the required fields!")

# End conversation button
if st.button("End Conversation"):
    st.write("🙏 Thank you for using TalentScout! We'll get back to you soon.")
import os
print("Hugging Face API Key:", os.getenv("HUGGINGFACE_API_KEY"))
