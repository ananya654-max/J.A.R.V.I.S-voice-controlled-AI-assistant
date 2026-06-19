import speech_recognition as sr
import pyttsx3
import datetime
import webbrowser
import os
import sys
import re

EXIT_COMMANDS = ["exit", "close", "stop", "goodbye"]

# Initialize text-to-speech engine
try:
    engine = pyttsx3.init()
    # Set properties
    engine.setProperty("rate", 170)  # Speed of speech
    engine.setProperty("volume", 1)  # Volume (0.0 to 1.0)
    # Check available voices
    voices = engine.getProperty('voices')
    if voices:
        engine.setProperty('voice', voices[0].id)
        print(f"Using voice: {voices[0].name}")
except Exception as e:
    print(f"Error initializing TTS engine: {e}")
    engine = None

def speak(text):
    try:
        print(f"Speaking: {text}")
        if engine:
            engine.say(text)
            engine.runAndWait()
        else:
            print("TTS engine not available, using fallback...")
            # Windows fallback: use PowerShell for text-to-speech
            os.system(f'PowerShell -Command "Add-Type -AssemblyName System.Speech; (New-Object System.Speech.Synthesis.SpeechSynthesizer).Speak(\'{text}\')"')
    except Exception as e:
        print(f"Error in speak: {e}")
        # Fallback to Windows TTS
        try:
            os.system(f'PowerShell -Command "Add-Type -AssemblyName System.Speech; (New-Object System.Speech.Synthesis.SpeechSynthesizer).Speak(\'{text}\')"')
        except Exception as e2:
            print(f"Fallback TTS also failed: {e2}")

def listen():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1
        audio = r.listen(source)
    try:
        command = r.recognize_google(audio, language="en-in")
        print(f"You said: {command}\n")
    except Exception:
        speak("Sorry, I didn't catch that.")
        return ""
    return command.lower()

def jarvis():
    speak("Hello Ananya, I am Jarvis. How can I help you?")
    while True:
        print("Waiting for command...")
        query = listen()
        print(f"Query received: '{query}'")

        if "time" in query:
            current_time = datetime.datetime.now().strftime("%H:%M:%S")
            speak(f"The time is {current_time}")

        elif "open youtube" in query:
            speak("Opening YouTube")
            webbrowser.open("https://youtube.com")

        elif "open google" in query:
            speak("Opening Google")
            webbrowser.open("https://google.com")

        elif "spotify" in query:
            spotify_url = None
            match = re.search(r'(https?://\S+)', query)
            if match:
                spotify_url = match.group(1)
            if not spotify_url:
                spotify_url = "https://open.spotify.com"

            speak("Opening Spotify")
            webbrowser.open(spotify_url)

        elif any(cmd in query for cmd in EXIT_COMMANDS):
            speak("Goodbye Ananya!")
            break

if __name__ == "__main__":
    jarvis()
