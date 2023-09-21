import socket
import select
import sys
import threading
import datetime
import os

<<<<<<< HEAD
# Criação da classe que representa a conexão do cliente, o nome dele, a mensagem eniviada e o horário que a mensagem foi enviada
class Message:
    def __init__(self, conn, client_name, message, currdatetime):
        self.conn = conn # Soquet de conexão do cliente
        self.client_name = client_name # Nome do cliente
        self.message = message # Mensagem do cliente
        self.currdatetime = currdatetime # Data e hora da mensagem enviada pelo cliente

# Criação das listagens de clientes e mensagens
clients = []
messages = []

# Função criada para enviar mensagem para os clientes, exceto o remetente
# Recebe como parâmetro a mensagem a ser enviada e a conexão do cliente que a enviou
def broadcast_message(message, sender_conn):
    # Percorre a lista de clientes para pegar a conexão de cada um
    for client_conn in clients:
        # Verifica se a conexão do cliente a ser verificado é diferente da conexão do cliente que enviou a mensagem
        if client_conn != sender_conn:
            try:
                # Se a conexão for diferente, então a mensagem será enviada
                client_conn.send(message.encode("utf-8"))
            except Exception as ex:
                # Caso dê erro, será exibida uma mensagem de erro genérica
                print("Error sending message to a client:", ex)

# Ordena as mensagens recebidas com base na data e hora que cada uma foi enviada e envia essas mensagens já ordenadas
# para um determinado cliente de uma conexão passada como parâmetro
def sort(conn):
    messages.sort(key=lambda x: x.currdatetime) # Ordena a lista de mensagens pela data e hora de cada uma
    for msg in messages:
        # Aqui a data é formatada para o nosso formato padrão
        strdatetime = msg.currdatetime.strftime("%d/%m/%Y, %H:%M:%S")
        # E agora as mensagens são enviadas para o determinado cliente da conexão passada como parâmetro
        conn.send(f"<{msg.client_name}, {strdatetime}>: {msg.message}".encode("utf-8"))

# Manda uma mensagem de "bye" e desconecta o cliente, alertando os demais clientes que ele saiu através da função "broadcast_message"
=======
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

>>>>>>> dc98ebd82413eecbdfc0c8f89529f9eb2ad8cd07
def logout(conn, client_name):
    conn.send("bye".encode("utf-8"))
    broadcast_message(f"{client_name} saiu.", conn)
    clients.remove(conn)

<<<<<<< HEAD
# Recebe um arquivo enviado por um cliente e o armazena no servidor
def upload(conn, client_name, message):
    data_file = message.split("|")

    # Verifica se o arquivo contém os 3 valores desejáveis
    if len(data_file) >= 3: #0 - UPLOAD; 1 - filename; 2 - data
        file_name = data_file[1]
        file_data = data_file[2]

        # Se houver mais partes na mensagem, as adiciona aos dados do arquivo
        if len(data_file) > 3:
            for data in data_file[3:]:
                file_data = file_data + "|" + data

        # Define o nome e o caminho onde o arquivo será salvo no servidor
        save_path = os.path.join("./uploads", file_name)

        # Abre o arquivo para escrita binária ('wb') e escreve os dados do arquivo
        with open(save_path, "wb") as file:
            file.write(file_data.encode("utf-8"))

        # Manda um aviso para os demais clientes que o cliente 'client_name' enviou um arquivo
        broadcast_message(f"<{client_name}>: enviou o arquivo: {file_name}", conn)

def download(conn, client_name, message):
    file_name = message.split("|")[1].strip()
    file_path = os.path.join("./uploads", file_name)
    if os.path.isfile(file_path):
        with open(file_path, "rb") as file:
            file_data = file.read()
        conn.send(file_data)
    else:
        conn.send("Arquivo não encontrado.".encode("utf-8"))

def chat_client(conn, addr, client_name):
    # Adiciona na lista de clientes o socket de conexão enviado como parâmetro
    clients.append(conn)
    # Define uma variável para controlar a conexão com o cliente
    client_connected = conn is not None
    try:
        # Enquanto o cliente estiver conectado
        while client_connected:
            # Recebe uma mensagem do cliente e a decodifica como UTF-8
            message = conn.recv(2048).decode("utf-8")
            if message:
                # Verifica se o cliente quer ordenar as mensagens
                if message.strip().upper() == '@ORDENAR':
                    sort(conn)
                # Verifica se o cliente quer sair do chat
                elif message.strip().upper() == '@SAIR':
                    logout(conn, client_name)
                # Verifica se o cliente quer fazer um upload de um arquivo
                elif message.split("|")[0].strip().upper() == '@UPLOAD':
                    upload(conn, client_name, message)
                # Verifica se o cliente quer fazer o download de um arquivo
                elif message.strip().upper() == '@DOWNLOAD':
                    download(conn, client_name, message)
                # Caso não seja nenhuma das alternativas anteriores, ele simplesmente irá criar uma nova instância de Message
                # e imprimir a mensagem para os demais clientes
=======
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
>>>>>>> dc98ebd82413eecbdfc0c8f89529f9eb2ad8cd07
                else:
                    timestamp = datetime.datetime.now().strftime("%H:%M:%S")
                    messages.append(Message(conn,client_name,message,datetime.datetime.now()))
                    if len(messages) > 15:
                        messages.pop(0)
                    print(f"<{addr},{client_name},{timestamp}>: {message}")
                    broadcast_message(f"<{client_name},{timestamp}>: {message}", conn)
            else:
                client_connected = False
<<<<<<< HEAD
    # Tratamento genérico para erros
    except Exception as ex:
        print("ERROR: ", ex)
    # Fecha a conexão do cliente
    conn.close()

# caso a porta já tenha sido atribuída será o prório valor de sys.argv[1], caso a porta ainda não tenha sido atribuída ela será 19000
port = int(sys.argv[1]) if len(sys.argv) > 1 else 19000

# Configura o servidor de socket e aceita conexões
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind(('0.0.0.0', port))
server.listen(5)

running = True
# Looping para aceitar novas conexões de clientes
while running:
    # Aceita uma nova conexão de cliente
    conn, addr = server.accept()
    # Recebe o nome do cliente da conexão e decodifica como UTF-8
    client_name = conn.recv(2048).decode("utf-8")

    #Inicia uma nova thread para lidar com a interação do cliente no chat
    client_thread = threading.Thread(target=chat_client, args=(conn, addr, client_name))
    client_thread.start()

# Fecha o servidor quando a execução termina
server.close()
=======
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

>>>>>>> dc98ebd82413eecbdfc0c8f89529f9eb2ad8cd07
