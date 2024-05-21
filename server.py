from socket import socket, gethostbyname, gethostname
from socket import AF_INET, SOCK_STREAM
import threading

SERVER = gethostbyname(gethostname())
PORT = 5050
ADDR = (SERVER, PORT)

FORMAT = 'utf-8'
HEADER = 64

# Commands
DISCONNECT_MSG  = "!disconnect"
CHANGE_NAME_MSG = "!name"

clients = {}
connections = []

server = socket(AF_INET, SOCK_STREAM)
server.bind(ADDR)
print(f"Server created in {SERVER}:{PORT}")

def send(msg, conn):
    size_msg = str(len(msg))
    size_msg += ' ' * (HEADER - len(size_msg))
    conn.send(size_msg.encode(FORMAT))
    conn.send(msg.encode(FORMAT))

def change_client_name(name, conn):
    print(f"[SERVER] {clients[conn]} change its name to {name}")
    clients[conn] = name

def handle_client(conn, addr):
    connected = True
    connections.append(conn)
    clients[conn] = addr[0]
    print(f"[SERVER] {addr[0]}:{addr[1]} connected")

    while connected:
        msg_size = conn.recv(HEADER).decode(FORMAT)
        if msg_size:
            msg_size = int(msg_size)
            msg = conn.recv(msg_size).decode(FORMAT)
            print(f"{clients[conn]}: {msg}")

            if msg == DISCONNECT_MSG:
                connected = False
                print(f"[SERVER] {clients[conn]} disconnected")
            
            elif msg.split(" ")[0] == CHANGE_NAME_MSG:
                change_client_name(msg.split(" ")[1], conn)

            for connection in clients.keys():
                if connection != conn: # if connection isn't the current client
                    send(f"{clients[conn]}: {msg}", connection)
    conn.close()
        
    
def start():
    print("[SERVER] STARTING")
    server.listen()
    print("[SERVER] LISTENING")
    
    while True:
        conn, addr = server.accept()    
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()
        
start()
