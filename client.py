import socket
import select
import sys

if len(sys.argv) < 2:
    print("usage: client NAME SERVER_IP [PORT]")
    sys.exit(1)

client_name = sys.argv[1]
ip_address = sys.argv[2]
port = int(sys.argv[3]) if len(sys.argv) > 3 else 19000

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.connect((ip_address, port))
server.send(client_name.encode("utf-8"))


running = True
while running:
    socket_list = [sys.stdin, server]
    
    rs, ws, es = select.select(socket_list, [], [])
    if es:
        print("ERR:", es)
    if ws:
        print("WRT:", ws)
    for sock in rs:
        if sock == server:
            message = sock.recv(2048).decode("utf-8")
            print(message)
            if message == "bye":
                running = False
                break
                
        else:
            message = sys.stdin.readline()
            if message.strip().upper() == '@UPLOAD':
                file_name = input("Informe o nome do arquivo: ")
                directory = input("Informe o diretório do arquivo: ")
                data = ""
                try:
                    with open(directory+"/"+file_name, "rb") as file:
                        data = file.read()
                    full_message = f"{message}|{file_name}|{data}"
                    size_in_bytes = sys.getsizeof(full_message.encode("utf-8"))
                    if size_in_bytes > 2048:
                        print("O tamanho limite do arquivo é 2048 bytes.")
                    else:
                        server.send(full_message.encode("utf-8"))
                except:
                    print("Erro ao ler arquivo.")
                    
            server.send(message.encode("utf-8"))
                
                

server.close()
