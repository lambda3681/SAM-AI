import pyaudio
import wave
import speech_recognition as sr
import pyttsx3
import tkinter as tk
import webbrowser
import os

def record_audio(filename="output.wav", duration=5, rate=44100, chunk=1024, channels=1):
    p = pyaudio.PyAudio()
    
    stream = p.open(format=pyaudio.paInt16,
                    channels=channels,
                    rate=rate,
                    input=True,
                    frames_per_buffer=chunk)
    
    print("Recording...")
    frames = []
    
    for _ in range(0, int(rate / chunk * duration)):
        data = stream.read(chunk)
        frames.append(data)
    
    print("Recording finished.")
    
    stream.stop_stream()
    stream.close()
    p.terminate()
    
    with wave.open(filename, 'wb') as wf:
        wf.setnchannels(channels)
        wf.setsampwidth(p.get_sample_size(pyaudio.paInt16))
        wf.setframerate(rate)
        wf.writeframes(b''.join(frames))
    
    print(f"Audio saved as {filename}")
    return filename


def search_web():
    speak("Please say your search query...")
    audio_file = record_audio(filename="search_query.wav", duration=5)
    query = recognize_speech(audio_file)
    if query:
        url = f"https://www.google.com/search?q={query}"
        webbrowser.open(url)
        print(f"Searching for: {query}")
    else:
        print("Could not understand the search query.")


def recognize_speech(filename):
    recognizer = sr.Recognizer()
    with sr.AudioFile(filename) as source:
        print("Processing audio for speech recognition...")
        audio_data = recognizer.record(source)
        try:
            text = recognizer.recognize_google(audio_data)
            print("Recognized Text:", text)
            return text
        except sr.UnknownValueError:
            print("Speech Recognition could not understand the audio.")
        except sr.RequestError:
            print("Could not request results from Google Speech Recognition service.")

def speak(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

class SAMApp:
    def __init__(self, root):
        self.root = root
        self.root.title("SAM AI")
        
        self.is_recording = False
        
        self.start_button = tk.Button(root, text="Start", command=self.start_recording)
        self.start_button.pack(pady=10)
        
        self.stop_button = tk.Button(root, text="Stop", command=self.stop_recording, state=tk.DISABLED)
        self.stop_button.pack(pady=10)
        
        self.status_label = tk.Label(root, text="Press Start to begin recording")
        self.status_label.pack(pady=10)
        
        self.audio_file = "output.wav"
    
    def start_recording(self):
        self.is_recording = True
        self.start_button.config(state=tk.DISABLED)
        self.stop_button.config(state=tk.NORMAL)
        self.status_label.config(text="Recording...")
        self.root.after(100, self.record_audio)
    
    def stop_recording(self):
        self.is_recording = False
        self.start_button.config(state=tk.NORMAL)
        self.stop_button.config(state=tk.DISABLED)
        self.status_label.config(text="Recording stopped. Processing audio...")
        recognized_text = recognize_speech(self.audio_file)
        if recognized_text:
            speak(f"You said: {recognized_text}")
            self.status_label.config(text=f"Recognized Text: {recognized_text}")
        else:
            self.status_label.config(text="Could not recognize any speech.")
    
    def record_audio(self):
        if self.is_recording:
            record_audio(self.audio_file, duration=5)
            self.stop_recording()

if __name__ == "__main__":
    # root = tk.Tk()
    # app = SAMApp(root)
    # root.mainloop()
    search_web()
