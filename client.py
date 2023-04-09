import socket
import pyaudio
import json
import base64
import asyncio
from ctypes import *

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
