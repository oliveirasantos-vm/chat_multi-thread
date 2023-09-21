import socket
import select
import sys

<<<<<<< HEAD
# Verifica se foram fornecidos argumentos de linha de comando adequados
=======
>>>>>>> dc98ebd82413eecbdfc0c8f89529f9eb2ad8cd07
if len(sys.argv) < 2:
    print("usage: client NAME SERVER_IP [PORT]")
    sys.exit(1)

<<<<<<< HEAD
# Atribui o nome do cliente, o endereço IP do servidor e a porta (caso a porta já tenha sido atribuída
# será o prório valor de sys.argv[3], caso a porta ainda não tenha sido atribuída ela será 19000)
=======
>>>>>>> dc98ebd82413eecbdfc0c8f89529f9eb2ad8cd07
client_name = sys.argv[1]
ip_address = sys.argv[2]
port = int(sys.argv[3]) if len(sys.argv) > 3 else 19000

<<<<<<< HEAD
# Cria um socket para se conectar ao servidor usando IPV4 (visto que estamos utilizando socket.AF_INET)
# e TCP (pois estamos utilizando socket.SOCK_STREAM)
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Conecta ao servidor usando o endereço IP e a porta especificados
server.connect((ip_address, port))

# Envia o nome do cliente para o servidor codificado em UTF-8
server.send(client_name.encode("utf-8"))

# Variável criada para iniciar o looping
running = True
while running:
    
    socket_list = [sys.stdin, server]
    
    # Verifica quais sockets estão prontos para leitura (rs), escrita (ws) e erro (es)
    rs, ws, es = select.select(socket_list, [], [])

    # Tratamento de erro
    if es:
        print("ERR:", es)

    # Tratamento de escrita
    if ws:
        print("WRT:", ws)

    # Tratamento de leitura
    for sock in rs:
        
        # Verifica se o socket é igual ao servidor
        if sock == server:
            
            # Recebe e mostra a mensagem do servidor
            message = sock.recv(2048).decode("utf-8")
            print(message)

            # Se a mensagem for "bye", o looping é encerrado
            if message == "bye":
                running = False
                break

            # Verifica se o usuário quer fazer upload de um arquivo
            if message.strip().upper() == '@UPLOAD':

                # Pede para o cliente informar o nome e o diretório do arquivo
=======
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
>>>>>>> dc98ebd82413eecbdfc0c8f89529f9eb2ad8cd07
                file_name = input("Informe o nome do arquivo: ")
                directory = input("Informe o diretório do arquivo: ")
                data = ""
                try:
<<<<<<< HEAD
                    # Lê os dados do arquivo binário e cria uma mensagem para enviar ao servidor
                    with open(directory + "/" + file_name, "rb") as file:
                        data = file.read()
                    full_message = f"{message}|{file_name}|{data}"
                    size_in_bytes = sys.getsizeof(full_message.encode("utf-8"))

                    # Verifica o tamanho da mensagem em bytes e envia ao servidor se for menor ou igual a 2048 bytes
=======
                    with open(directory+"/"+file_name, "rb") as file:
                        data = file.read()
                    full_message = f"{message}|{file_name}|{data}"
                    size_in_bytes = sys.getsizeof(full_message.encode("utf-8"))
>>>>>>> dc98ebd82413eecbdfc0c8f89529f9eb2ad8cd07
                    if size_in_bytes > 2048:
                        print("O tamanho limite do arquivo é 2048 bytes.")
                    else:
                        server.send(full_message.encode("utf-8"))
                except:
                    print("Erro ao ler arquivo.")
<<<<<<< HEAD
            elif message.startswith('@FILE:'):
                # Extrai o nome do arquivo da mensagem
                file_name = message.split(':')[1].strip()

                # Recebe os dados do arquivo do servidor
                file_data = sock.recv(2048)

                # Salva o arquivo no sistema de arquivos local
                with open(file_name, 'wb') as file:
                    file.write(file_data)
                print(f"Arquivo '{file_name}' recebido e salvo com sucesso.")

            else:
                print(message)

        # Se o socket não for igual ao servidor
        else:
            message = sys.stdin.readline()
                    
            # Envia a mensagem ao servidor
            server.send(message.encode("utf-8"))
                
                
# Fecha o socket do cliente quando o loop termina
server.close()
=======
                    
            server.send(message.encode("utf-8"))
                
                

server.close()
>>>>>>> dc98ebd82413eecbdfc0c8f89529f9eb2ad8cd07
