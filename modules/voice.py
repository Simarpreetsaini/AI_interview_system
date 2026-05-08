from gtts import gTTS
import streamlit as st
import base64

def speak(text):

    tts = gTTS(text=text, lang="en")
    filename = "question_voice.mp3"
    tts.save(filename)

    audio_file = open(filename, "rb")
    audio_bytes = audio_file.read()

    b64 = base64.b64encode(audio_bytes).decode()

    audio_html = f"""
    <audio autoplay>
    <source src="data:audio/mp3;base64,{b64}" type="audio/mp3">
    </audio>
    """

    st.markdown(audio_html, unsafe_allow_html=True)