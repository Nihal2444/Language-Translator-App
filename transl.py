import tkinter as tk
from tkinter import Menu
from translate import Translator
from PIL import Image, ImageTk
from gtts import gTTS
import pygame
import tempfile
import os
import pyaudio
import wave
import speech_recognition as sr

# Initialize pygame mixer
pygame.mixer.init()

# Create the main window
root = tk.Tk()
root.geometry("650x450")
root.title("Language Translator")

# Set up background image
image_path = r"C:\Users\nihal\OneDrive\Desktop\Translator.jpg"
image_image = Image.open(image_path)
image_resized = image_image.resize((650, 450), Image.BILINEAR)
image_tk = ImageTk.PhotoImage(image_resized)
image_label = tk.Label(root, image=image_tk, bg="#6B71FF")
image_label.image = image_tk
image_label.place(x=-1, y=-1)

# Function to create a dropdown menu
def create_language_menu(button, variable):
    menu = Menu(button, tearoff=0)
    for lang in ["English", "French", "Arabic", "Malayalam", "Hindi", "Chinese", "Korean"]:
        menu.add_radiobutton(label=lang, variable=variable, value=lang)
    button["menu"] = menu

# Function to perform translation
def translate_text():
    src_lang = left_language.get()
    dest_lang = right_language.get()
    text_to_translate = left_entry.get("1.0", "end-1c")

    language_map = {
        "English": "en",
        "French": "fr",
        "Arabic": "ar",
        "Malayalam": "ml",
        "Hindi": "hi",
        "Chinese": "zh",
        "Korean": "ko"
    }

    src_lang_code = language_map.get(src_lang)
    dest_lang_code = language_map.get(dest_lang)

    if src_lang_code and dest_lang_code:
        translator = Translator(from_lang=src_lang_code, to_lang=dest_lang_code)
        translation = translator.translate(text_to_translate)
        right_entry.delete("1.0", "end")
        right_entry.insert("1.0", translation)
    else:
        error_msg = "Translation not supported for selected languages"
        right_entry.insert("1.0", error_msg)

# Function to speak text using gTTS
def speak_text(text, lang):
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as temp_audio:
        tts = gTTS(text=text, lang=lang, slow=False)
        temp_audio_path = temp_audio.name
        tts.save(temp_audio_path)
    pygame.mixer.music.load(temp_audio_path)
    pygame.mixer.music.play()

# Function to play voice when button is clicked
def play_voice():
    text = right_entry.get("1.0", "end-1c")
    lang = right_language.get().lower()
    lang_map = {
        "english": "en",
        "french": "fr",
        "arabic": "ar",
        "malayalam": "ml",
        "hindi": "hi",
        "chinese": "zh",
        "korean": "ko"
    }
    speak_text(text, lang_map.get(lang, "en"))

# Function to record audio
def record_audio():
    chunk = 1024  # Record in chunks of 1024 samples
    sample_format = pyaudio.paInt16  # 16 bits per sample
    channels = 1
    fs = 44100  # Record at 44100 samples per second
    seconds = 5
    filename = "recorded.wav"

    p = pyaudio.PyAudio()  # Create an interface to PortAudio

    print('Recording')

    stream = p.open(format=sample_format,
                    channels=channels,
                    rate=fs,
                    frames_per_buffer=chunk,
                    input=True)

    frames = []  # Initialize array to store frames

    # Store data in chunks for 5 seconds
    for _ in range(0, int(fs / chunk * seconds)):
        data = stream.read(chunk)
        frames.append(data)

    # Stop and close the stream
    stream.stop_stream()
    stream.close()
    # Terminate the PortAudio interface
    p.terminate()

    print('Recording finished')

    # Save the recorded data as a WAV file
    wf = wave.open(filename, 'wb')
    wf.setnchannels(channels)
    wf.setsampwidth(p.get_sample_size(sample_format))
    wf.setframerate(fs)
    wf.writeframes(b''.join(frames))
    wf.close()

    # Transcribe the recorded audio to text
    r = sr.Recognizer()
    with sr.AudioFile(filename) as source:
        audio_data = r.record(source)
        text = r.recognize_google(audio_data)
        left_entry.delete("1.0", "end")
        left_entry.insert("1.0", text)

# StringVar for language selection
left_language = tk.StringVar(root)
right_language = tk.StringVar(root)
left_language.set("English")  # default value
right_language.set("French")  # default value

# Create the "Select Language" button for the left entry field
left_select_language_button = tk.Menubutton(root, text="Select Language ^", relief="raised")
left_select_language_button.place(x=10, y=180, width=120)
create_language_menu(left_select_language_button, left_language)

# Create the "Select Language" button for the right entry field
right_select_language_button = tk.Menubutton(root, text="Select Language ^", relief="raised")
right_select_language_button.place(x=350, y=180, width=120)
create_language_menu(right_select_language_button, right_language)

# Create the left entry field
left_entry = tk.Text(root, height=10, width=40, font=("Helvetica", 14))
left_entry.place(x=10, y=220, height=80, width=250)

# Create the right entry field
right_entry = tk.Text(root, height=10, width=40, font=("Helvetica", 14))
right_entry.place(x=350, y=220, height=80, width=250)

# Create the Translate button
translate_button = tk.Button(root, text="Translate", font=("Helvetica", 14), command=translate_text)
translate_button.place(x=270, y=390)

# Create the Play Voice button
play_voice_button = tk.Button(root, text="Play Voice", font=("Helvetica", 10), command=play_voice)
play_voice_button.place(x=520, y=190)

# Create the Record button
record_button = tk.Button(root, text="Record", font=("Helvetica", 10), command=record_audio)
record_button.place(x=10, y=310)

# Start the Tkinter event loop
root.mainloop()
