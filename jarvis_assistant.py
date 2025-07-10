import os
import sys
import pvporcupine
import sounddevice as sd
import vosk
import queue
import json
import pyttsx3
import wave

# Get base folder (for .exe or script)
BASE_DIR = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))

# Paths
KEYWORD_PATH = os.path.join(BASE_DIR, "jarvis.ppn")
WAKEWORD_MODEL = os.path.join(BASE_DIR, "porcupine_params.pv")
VOSK_MODEL_PATH = os.path.join(BASE_DIR, "vosk-model-en-us-daanzu-20200328")
DLL_PATH = os.path.join(BASE_DIR, "libpv_porcupine.dll")

# Wake word init
porcupine = pvporcupine.create(
    access_key="1ryccezDqIqB4kzrxVXtUsV9lgVLSvfvN0jbOiZFqElyvnIMFkz0/g==",
    keyword_paths=[KEYWORD_PATH]
)

# TTS init
engine = pyttsx3.init()
engine.setProperty("rate", 150)

def speak(text):
    print(f"Jarvis: {text}")
    engine.say(text)
    engine.runAndWait()

# Voice recognition init
model = vosk.Model(VOSK_MODEL_PATH)
q = queue.Queue()

def callback(indata, frames, time, status):
    if status:
        print(status, file=sys.stderr)
    q.put(bytes(indata))

speak("Jarvis is online.")

# Wake loop
with sd.RawInputStream(samplerate=porcupine.sample_rate, blocksize=porcupine.frame_length, dtype='int16', channels=1, callback=callback):
    while True:
        pcm = q.get()
        pcm = memoryview(pcm).cast('h')
        keyword_index = porcupine.process(pcm)
        if keyword_index >= 0:
            speak("Yes sir?")
            break

# Start listening for command
recognizer = vosk.KaldiRecognizer(model, 16000)
with sd.RawInputStream(samplerate=16000, blocksize=8000, dtype='int16', channels=1, callback=callback):
    while True:
        data = q.get()
        if recognizer.AcceptWaveform(data):
            result = json.loads(recognizer.Result())
            text = result.get("text", "").lower()
            if not text:
                speak("I didn’t understand that, sir.")
                continue

            print("You said:", text)

            if "your name" in text:
                speak("I am Jarvis, your assistant.")
            elif "time" in text:
                from datetime import datetime
                now = datetime.now().strftime("%I:%M %p")
                speak(f"The time is {now}")
            elif "exit" in text or "goodbye" in text:
                speak("Goodbye, sir.")
                break
            else:
                speak("I didn’t understand that, sir.")
