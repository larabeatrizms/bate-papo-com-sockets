# UNIVERSIDADE FEDERAL DO RIO GRANDE DO NORTE
# DEPARTAMENTO DE ENGENHARIA DE COMPUTACAO E AUTOMACAO
# DISCIPLINA REDES DE COMPUTADORES (DCA0113)
# AUTORES: Francisco Kennedi
#          Lara Beatriz
# SCRIPT: Chat com servidor (Servidor)
#

# importacao das bibliotecas
from socket import *  # sockets
import threading

# definindo dicionario para guardar ip do cliente e nickname
dict_nickname = dict()


def on_client(key, nickname):
    information_on_client = nickname.decode('utf-8') + ' entrou na sala'
    dict_nickname[key] = nickname.decode('utf-8')
    print(information_on_client)
    return information_on_client


def out_client(key, nickname):
    dict_nickname.pop(key, nickname)
    information_client_out = nickname + " saiu."
    for client in dict_nickname:
        if client != key:
            client.send(information_client_out.encode('utf-8'))
    return information_client_out


def change_nick(key, nickname):
    current_name = dict_nickname[key]
    dict_nickname[key] = nickname.decode('utf-8')
    return current_name + " alterou o nome para " + nickname


def client_says(key, message):
    if message != 'quit':
        return dict_nickname[key] + ': ' + message


def client_list(addr):
    string = 'Os clientes conectados são: \n'
    for client in dict_nickname:
        string += '[<' + dict_nickname[client] + '> <' + str(addr[0]) + '> <' + str(addr[1]) + '>] \n'
    return string


def write_file(message):
    f = open('historico.txt', 'a')
    f.write(message + '\n')
    f.close()


def send_history(conn):
    f = open('historico.txt', 'r')
    historico = f.read()
    conn.send(historico.encode('utf-8'))
    f.close()


def connect_client(conn, addr):
    nickname = conn.recv(1024)
    print('Nick é ' + str(nickname.decode('utf-8')))
    print(on_client(conn, nickname))
    for client in dict_nickname:
        if client != conn:
            client.send(on_client(conn, nickname).encode('utf-8'))
#   send_history(conn)
    write_file(on_client(conn, nickname))
    message = ''
    while message != 'quit':
        message = conn.recv(1024).decode('utf-8')  # recebe dados do cliente
        if not message:
            break
        if client_says(conn, message) is not None:
            print(client_says(conn, message))
            write_file(client_says(conn, message))
            #se a mensagem for um comando executa tais comandos, se não manda pra todos os usuários:
            if message.find("(") != -1 and message.find(")") != -1:
                # "split" divide a frase para pegar o comando
                command = message.split('(') #pega só o comando
                user_destiny = command[1].split(')') #pega o usuário de destino
                if command[0] == 'nome':
                    print(change_nick(conn, message))
                elif command[0] == 'lista':
                    conn.send(client_list(addr).encode('utf-8')) #Lista todos os usuários conectados
                elif command[0] == 'privado':
                    user_destiny = user_destiny[0]
                    for client in dict_nickname:
                        if dict_nickname[client] == user_destiny:
                            sala_pvd = True
                            nick_pvd = user_destiny
                            nick_con = dict_nickname[conn]
                            string = dict_nickname[conn] \
                                     + ' iniciou um privado. Digite *privado(' \
                                     + dict_nickname[conn] \
                                     + ') para continuar e *quit pvd* para sair.'
                            client.send(string.encode('utf-8'))
                            print('Modo Privado ativado entre ' + nick_con + ' e ' + nick_pvd)
                            #loop do privado entre os usuários
                            while sala_pvd == True:
                                message = conn.recv(1024).decode('utf-8')
                                if message == 'quit pvd':
                                    sala_pvd = False;
                                print(client_says(conn, message))
                                client.send(client_says(conn, message).encode('utf-8'))

            else:
                for client in dict_nickname:
                    if client != conn:
                        client.send(client_says(conn, message).encode('utf-8'))
    print(out_client(conn, dict_nickname[conn]))
    conn.close()


def listener_clients():

    while True:
        conn, addr = serverSocket.accept() #aceita as conexões dos clientes
        threading.Thread(target=connect_client, args=(conn, addr,)).start()

    serverSocket.close() #encerra o socket do servidor

"""
Configurando o servidor
"""
serverName = ''  # ip do servidor (em branco)
serverPort = 65000  # porta a se conectar
serverSocket = socket(AF_INET, SOCK_STREAM)  # criacao do socket TCP
serverSocket.bind((serverName, serverPort))  # bind do ip do servidor com a porta
serverSocket.listen(1)  # socket pronto para 'ouvir' conexoes
print('Servidor TCP esperando conexoes na porta %d ...' % (serverPort))
file = open('historico.txt', 'w')
file.write('')
file.close()
listener_clients()  # Chama função para escutar os clientes

# while 1:
#     connectionSocket, addr = serverSocket.accept()  # aceita as conexoes dos clientes
#     message = connectionSocket.recv(1024)  # recebe dados do cliente
#     print(connectionSocket.fileno())
#     print(on_client(addr, message))
#     print(dict_nickname)
#     while message != 'quit':
#         print('Cliente %s enviou: %s' % (addr, message))
#         message = connectionSocket.recv(1024)
#         if not message:
#             break
#         connectionSocket.send(message)  # envia para o cliente o texto transformado
#         # print("Lista de clientes conectados: ", str(lista_addr))

