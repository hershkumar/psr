import socket
import pyaudio
import speech_recognition as sr
from ctypes import *
import threading

# error handling for ALSA
ERROR_HANDLER_FUNC = CFUNCTYPE(None, c_char_p, c_int, c_char_p, c_int, c_char_p)
def py_error_handler(filename, line, function, err, fmt):
    pass
c_error_handler = ERROR_HANDLER_FUNC(py_error_handler)

asound = cdll.LoadLibrary('libasound.so')
# Set error handler
asound.snd_lib_error_set_handler(c_error_handler)



HOST = "senbonzakura"
PORT = 8080

print("Opening audio stream...")
# open the audio stream from the microphone
p = pyaudio.PyAudio()
audio_stream = p.open(
    frames_per_buffer=3200,
    rate=48000,
    format=pyaudio.paInt16,
    channels=1,
    input=True,
)

print("Audio stream opened. Connecting to server...")

transcriptions = []

def server_client():
    # connect to the server.py socket
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((HOST, PORT))
    message = input(" -> ")  # take input

    while message.lower().strip() != 'bye':
        s.send(message.encode())  # send message
        data = s.recv(1024).decode()  # receive response

        print('Received from server: ' + data)  # show in terminal

        message = input(" -> ")  # again take input

    s.close()  # close the connection

def transcribe_audio():
    # transcribe the audio stream
    print("Transcribing audio stream...")
    r = sr.Recognizer()
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source)
        print("Say something!")
        audio = r.listen(source)
        transcription = r.recognize_vosk(audio)
        print(transcription)


server_thread = threading.Thread(target=server_client)
# transcription_thread = threading.Thread(target=transcribe_audio)

# transcription_thread.start()
transcribe_audio()

# server_thread.start()
