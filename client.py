from socket import socket
from socket import AF_INET, SOCK_STREAM
import threading

SERVER = "127.0.1.1"
PORT = 5050
ADDR = (SERVER, PORT)

FORMAT = 'utf-8'
HEADER = 64

client = socket(AF_INET, SOCK_STREAM)
client.connect(ADDR)
print(f"You has been connected to {SERVER}:{PORT}")

def send(msg):
    size_msg = str(len(msg))
    size_msg += ' ' * (HEADER - len(size_msg))
    client.send(size_msg.encode(FORMAT))
    client.send(msg.encode(FORMAT))

def handle_input():
    while True:
        message = str(input(""))
        send(message)

def handle_listen():
    while True:
        msg_size = client.recv(HEADER).decode(FORMAT)
        if msg_size:
            msg_size = int(msg_size)
            msg = client.recv(msg_size).decode(FORMAT)
            print(f"{msg}")
            

thread = threading.Thread(target=handle_listen)
thread.start()
handle_input()


