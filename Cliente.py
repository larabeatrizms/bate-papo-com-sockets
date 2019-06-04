# UNIVERSIDADE FEDERAL DO RIO GRANDE DO NORTE
# DEPARTAMENTO DE ENGENHARIA DE COMPUTACAO E AUTOMACAO
# DISCIPLINA REDES DE COMPUTADORES (DCA0113)
# AUTORES: Francisco Kennedi
#          Lara Beatriz
# SCRIPT: Chat com servidor (Cliente)
#

# importacao das bibliotecas
from socket import *
import threading

# definicao das variaveis
serverName = 'localhost' # ip do servidor
serverPort = 65000  # porta a se conectar
clientSocket = socket(AF_INET,SOCK_STREAM) # criacao do socket TCP
clientSocket.connect((serverName, serverPort)) # conecta o socket ao servidor
message = ''
nickname = input('Digite o seu nome: ')
clientSocket.send(nickname.encode('utf-8'))
print('Bem vindo, pode começar a conversar!\n')


def print_messages(message):
    while message != 'quit':
        received_messages = clientSocket.recv(1024)
        print(received_messages.decode('utf-8'))
    return 0


while message != 'quit':
    clientSocket.send(message.encode('utf-8'))
    threading.Thread(target=print_messages, args=(message,)).start()
    message = input()


clientSocket.send(message.encode('utf-8'))
clientSocket.close()
