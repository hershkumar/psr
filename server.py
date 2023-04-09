import socket
import threading

HOST = "senbonzakura"
PORT = 8080

# run the socket server in a thread
def process():
    # run a socket server
    print("Starting socket server...")
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    s.bind((socket.gethostname(), PORT))
    s.listen(1)
    
    print("Socket server initialized. Waiting for connection...")
    conn, addr = s.accept()
    print("Connected by", addr)
    while True:
        data = conn.recv(1024).decode()
        if not data:
            break
        print("Received", data)
        data = input("Enter data to send: ")
        conn.send(data.encode())
    print("Closing connection...")
    conn.close()


def start_server():
    # run the thread to start the server
    t = threading.Thread(target=process)
    t.start()

start_server()