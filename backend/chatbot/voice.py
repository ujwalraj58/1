from gtts import gTTS
import speech_recognition as sr
import os
import time

def speak(text):
    timestamp = int(time.time())
    filename = f"response_{timestamp}.mp3"
    tts = gTTS(text)
    tts.save(filename)

    try:
        if os.name == 'nt':  # Windows
            os.system(f"start {filename}")
        elif os.name == 'posix':  # macOS/Linux
            os.system(f"afplay {filename}")  # macOS
    except Exception as e:
        print("Could not play audio:", e)

def listen():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("🎤 Listening... Speak your question")
        audio = recognizer.listen(source)

    try:
        print("🔄 Recognizing...")
        query = recognizer.recognize_google(audio)
        print("📝 You said:", query)
        return query
    except sr.UnknownValueError:
        return "Sorry, I couldn’t understand your voice."
    except sr.RequestError:
        return "Speech service is down."
