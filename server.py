import socket
import select
import sys
import threading
import datetime
import os

class Message:
    def __init__(self, conn, client_name, message, currdatetime):
        self.conn = conn
        self.client_name = client_name
        self.message = message
        self.currdatetime = currdatetime

clients = []
messages = []

def broadcast_message(message, sender_conn):
    for client_conn in clients:
        if client_conn != sender_conn:
            try:
                client_conn.send(message.encode("utf-8"))
            except Exception as ex:
                print("Error sending message to a client:", ex)

def sort(conn):
    messages.sort(key=lambda x: x.currdatetime)
    for msg in messages:
        strdatetime = msg.currdatetime.strftime("%d/%m/%Y, %H:%M:%S")
        conn.send(f"<{msg.client_name}, {strdatetime}>: {msg.message}".encode("utf-8"))

def logout(conn, client_name):
    conn.send("bye".encode("utf-8"))
    broadcast_message(f"{client_name} saiu.", conn)
    clients.remove(conn)

def upload(conn, client_name, message):
    data_file = message.split("|")
    if len(data_file) >= 3: #0 - UPLOAD; 1 - filename; 2 - data
        file_name = data_file[1]
        file_data = data_file[2]
        if len(data_file) > 3:
            for data in data_file[3:]:
                file_data = file_data + "|" + data
        save_path = os.path.join("./uploads", file_name)
        with open(save_path, "wb") as file:
            file.write(file_data.encode("utf-8"))
        broadcast_message(f"<{client_name}>: enviou o arquivo: {file_name}",None)

def download():
    print("")

def chat_client(conn, addr, client_name):
    clients.append(conn)
    client_connected = conn is not None
    try:
        while client_connected:
            message = conn.recv(2048).decode("utf-8")
            if message:
                if message.strip().upper() == '@ORDENAR':
                    sort(conn)
                elif message.strip().upper() == '@SAIR':
                    logout(conn, client_name)
                elif message.split("|")[0].strip().upper() == '@UPLOAD':
                    upload(conn, client_name, message)
                elif message.strip().upper() == '@DOWNLOAD':
                    print(message)
                else:
                    timestamp = datetime.datetime.now().strftime("%H:%M:%S")
                    messages.append(Message(conn,client_name,message,datetime.datetime.now()))
                    if len(messages) > 15:
                        messages.pop(0)
                    print(f"<{addr},{client_name},{timestamp}>: {message}")
                    broadcast_message(f"<{client_name},{timestamp}>: {message}", conn)
            else:
                client_connected = False
    except Exception as ex:
        print("ERROR: ", ex)
    conn.close()


        

port = int(sys.argv[1]) if len(sys.argv) > 1 else 19000

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

server.bind(('0.0.0.0', port))

server.listen(5)

running = True
while running:
    conn, addr = server.accept()
    client_name = conn.recv(2048).decode("utf-8")
    client_thread = threading.Thread(target=chat_client, args=(conn, addr, client_name))
    client_thread.start()

server.close()

